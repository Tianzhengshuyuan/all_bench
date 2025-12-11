import re
import os
import pickle
import numpy as np
import pandas as pd
from tqdm import trange
import argparse
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from itertools import combinations

# ===================== 日志解析正则 =====================
pattern1 = re.compile(
    r"总题组数:\s*\d+.*?第一轮正确答案数:\s*\d+.*?正确率:\s*[\d.]+%.*?第二轮正确答案数:\s*\d+.*?正确率:\s*([\d.]+)%"
)
pattern2 = re.compile(
    r"总题数:\s*\d+.*?正确数:\s*\d+.*?正确率:\s*([\d.]+)%,\s*耗时:"
)


# ===================== 函数：读取准确率 =====================
def get_accuracies(logfile, max_samples=None):
    accuracies = []
    with open(logfile, "r", encoding="utf-8") as f:
        for line in f:
            m1 = pattern1.search(line)
            if m1:
                acc = float(m1.group(1)) / 100.0
                accuracies.append(acc)
                if max_samples and len(accuracies) >= max_samples:
                    break
                continue
            m2 = pattern2.search(line)
            if m2:
                acc = float(m2.group(1)) / 100.0
                accuracies.append(acc)
                if max_samples and len(accuracies) >= max_samples:
                    break
    return np.array(accuracies)


# ===================== 特征预处理: one-hot for 分类变量 =====================
def preprocess_features(df, target_col="accuracy"):
    """
    将分类变量展开为one-hot编码，保持数值型变量不变。
    """
    feature_cols = [c for c in df.columns if c != target_col]
    categorical_cols = [c for c in feature_cols if df[c].dtype == object or str(df[c].dtype).startswith("category")]
    numeric_cols = [c for c in feature_cols if c not in categorical_cols]

    df_processed = pd.get_dummies(df[feature_cols], columns=categorical_cols, drop_first=True)
    return df_processed, numeric_cols, categorical_cols


# ===================== 构建设计矩阵（主效应+交互，避免同类dummy交互） =====================
def build_design_matrix(df, feature_cols):
    """
    输入: 已经过 one-hot 编码的数据框
    输出: (X, all_terms)
    - 主效应
    - 跨变量组的交互（同一原始特征的哑变量之间不交互）
    """
    X_dict = {}

    # 建立 group 信息: language_xx -> language
    col2group = {}
    for col in feature_cols:
        if "_" in col:  # one-hot 展开的
            group = col.split("_", 1)[0]
        else:
            group = col
        col2group[col] = group

    # 主效应
    for col in feature_cols:
        X_dict[col] = df[col].values

    # 两两交互：仅允许不同组之间
    for col1, col2 in combinations(feature_cols, 2):
        if col2group[col1] != col2group[col2]:
            X_dict[f"{col1} x {col2}"] = df[col1].values * df[col2].values

    X = pd.DataFrame(X_dict)
    return X.values, list(X_dict.keys())


# ===================== 计算 partial R² (每个term的η²) =====================
def compute_effects(X, y, terms):
    """对每个term计算partial R²"""
    model_full = LinearRegression().fit(X, y)
    r2_full = r2_score(y, model_full.predict(X))

    effect_results = []
    for i, term in enumerate(terms):
        # 去掉该term，重新拟合
        idx = [j for j in range(X.shape[1]) if j != i]
        X_reduced = X[:, idx]
        model_reduced = LinearRegression().fit(X_reduced, y)
        r2_reduced = r2_score(y, model_reduced.predict(X_reduced))

        # partial R² = R²_full - R²_reduced
        eff = max(r2_full - r2_reduced, 0.0)
        effect_results.append((term, eff))
    return dict(effect_results), r2_full


# ===================== permutation test =====================
def permutation_test_linear(X, y, terms, n_perm=200):
    """线性模型+permutation test"""
    obs_effects, r2_full = compute_effects(X, y, terms)
    print(f"[DEBUG] 全模型 R²: {r2_full:.6f}")
    null_effects = {t: [] for t in terms}

    for _ in trange(n_perm, desc="Permutation (Linear)"):
        y_perm = np.random.permutation(y)
        perm_effects, _ = compute_effects(X, y_perm, terms)
        for t in terms:
            null_effects[t].append(perm_effects[t])

    results = []
    for t in terms:
        obs_val = obs_effects[t]
        perm_vals = np.array(null_effects[t])
        p = np.mean(perm_vals >= obs_val)
        results.append({
            "term": t,
            "eta2_obs": obs_val,
            "eta2_perm_mean": perm_vals.mean(),
            "p_value": p
        })
    return pd.DataFrame(results)


# ===================== 主流程 =====================
def main(args):
    # 1. 读取设计矩阵
    with open(args.pkl_path, "rb") as f:
        design_list = pickle.load(f)[: args.sample_num]
    df_design = pd.DataFrame(design_list)

    # 2. 加载准确率
    accuracies = get_accuracies(args.logfile, max_samples=args.sample_num)
    if len(accuracies) != args.sample_num:
        raise ValueError(f"预计 {args.sample_num} 个准确率，实际得到 {len(accuracies)} 个，请检查日志文件")
    df_design["accuracy"] = accuracies

    y = df_design["accuracy"].values

    # 3. 特征预处理：分类变量 -> one-hot
    df_features, numeric_cols, categorical_cols = preprocess_features(df_design, target_col="accuracy")
    print(f"[DEBUG] 数值型特征: {numeric_cols}")
    print(f"[DEBUG] 分类变量: {categorical_cols}")
    print(f"[DEBUG] one-hot 后列数: {df_features.shape[1]}")

    # 4. 构建设计矩阵（主效应+交互，但剔除同组dummy交互）
    X, terms = build_design_matrix(df_features, df_features.columns)

    # 5. permutation test
    res = permutation_test_linear(X, y, terms, n_perm=args.n_perm)

    # ==== 输出 ====
    pd.set_option("display.max_rows", None)
    pd.set_option("display.width", 2000)
    print("\n==== 线性模型 permutation test 结果 ====")
    with pd.option_context("display.float_format", "{:.6f}".format):
        print(res.sort_values(by=["p_value", "eta2_obs"], ascending=[True, False]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="线性模型 + permutation test (主效应+交互)")
    parser.add_argument("--logfile", type=str, default="log/anova_kimiv1.log")
    parser.add_argument("--pkl_path", type=str, default="L36_design.pkl")
    parser.add_argument("--sample_num", type=int, default=36)
    parser.add_argument("--n_perm", type=int, default=200)
    args = parser.parse_args()
    main(args)