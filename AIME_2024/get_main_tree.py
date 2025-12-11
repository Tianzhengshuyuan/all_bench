import re
import os
import pickle
import numpy as np
import pandas as pd
import shap
from tqdm import trange
import argparse
from xgboost import XGBRegressor

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


# ===================== SHAP 计算 =====================
def compute_shap_importance(model, X, feature_names):
    """返回全局SHAP主效应和交互效应（忽略language_xxx之间的交互）"""
    explainer = shap.TreeExplainer(model)
    shap_vals = explainer.shap_values(X)   # (n_samples, n_features)
    inter_vals = explainer.shap_interaction_values(X) #(n_samples, n_features, n_features)

    # 主效应
    main_effects = np.abs(shap_vals).mean(axis=0)
    main_df = pd.DataFrame({
        "factor": feature_names,
        "importance_obs": main_effects
    })

    inter_effects = np.abs(inter_vals).mean(axis=0)
    inter_list = []
    
    if args.merge_language:
        for i in range(len(feature_names)):
            for j in range(i+1, len(feature_names)):
                inter_list.append({
                    "factor_pair": f"{feature_names[i]} x {feature_names[j]}",
                    "importance_obs": inter_effects[i, j]
                })
    else:    
        # 交互效应：排除 language_xxx 与 language_yyy 的组合
        for i in range(len(feature_names)):
            for j in range(i+1, len(feature_names)):
                fi, fj = feature_names[i], feature_names[j]
                # 如果两个变量都以 "language_" 开头，就跳过
                if fi.startswith("language_") and fj.startswith("language_"):
                    continue
                inter_list.append({
                    "factor_pair": f"{fi} x {fj}",
                    "importance_obs": inter_effects[i, j]
                })
    inter_df = pd.DataFrame(inter_list)
    return main_df, inter_df

# ===================== Permutation Test =====================
def permutation_test_shap(X, y, feature_names, n_perm=200):
    """Permutation test for SHAP 主效应与交互效应 (使用 categorical 特征支持)"""
    # 原始模型
    model = XGBRegressor(n_estimators=200, max_depth=6, random_state=42,
                         enable_categorical=True, verbosity=0)
    model.fit(X, y)
    main_obs, inter_obs = compute_shap_importance(model, X, feature_names)

    # 观测值
    obs_main = dict(zip(main_obs["factor"], main_obs["importance_obs"]))
    obs_inter = dict(zip(inter_obs["factor_pair"], inter_obs["importance_obs"]))

    # null 分布
    null_main = {f: [] for f in obs_main}
    null_inter = {f: [] for f in obs_inter}

    for _ in trange(n_perm, desc="Permutation"):
        y_perm = np.random.permutation(y)
        model_perm = XGBRegressor(n_estimators=200, max_depth=6, random_state=42,
                                  enable_categorical=True, verbosity=0)
        model_perm.fit(X, y_perm)
        main_df, inter_df = compute_shap_importance(model_perm, X, feature_names)

        for f, val in zip(main_df["factor"], main_df["importance_obs"]):
            null_main[f].append(val)
        for f, val in zip(inter_df["factor_pair"], inter_df["importance_obs"]):
            null_inter[f].append(val)

    # 计算 p 值
    main_results = []
    for f, obs_val in obs_main.items():
        perm_vals = np.array(null_main[f])
        p = np.mean(perm_vals >= obs_val) # perm_vals 数组里的数比obs_val大的比例
        main_results.append({
            "name": f, "importance_obs": obs_val,
            "importance_perm": perm_vals.mean(), "p_value": p, "type": "main"
        })

    inter_results = []
    obs_sum = 0
    for f, obs_val in obs_inter.items():
        obs_sum += obs_val
        perm_vals = np.array(null_inter[f])
        p = np.mean(perm_vals >= obs_val)
        inter_results.append({
            "name": f, "importance_obs": obs_val,
            "importance_perm": perm_vals.mean(), "p_value": p, "type": "interaction"
        })
    print(f"[DEBUG] 交互效应总重要性: {obs_sum:.6f}")
    return pd.DataFrame(main_results), pd.DataFrame(inter_results)

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

    # 3. 特征预处理: 转 categorical codes
    feature_cols = [c for c in df_design.columns if c != "accuracy"]
    X = df_design[feature_cols].copy()
    if args.merge_language:
        for col in feature_cols:
            print(f"[DEBUG] {col} 原始类型: {X[col].dtype}")  # 输出当前列类型
            if X[col].dtype == object or str(X[col].dtype).startswith("category"):
                X[col] = pd.Categorical(X[col]).codes
                X[col] = X[col].astype("int64")
                print(f"[DEBUG] {col} 转换后类型: {X[col].dtype}")  # 输出转换后的类型
    else:
        # 特殊处理 language 列 -> one-hot
        if "language" in X.columns:
            mapping = ["yy", "zw", "ry", "ey", "fy", "alby"]
            for val in mapping:
                col_name = f"language_{val}"
                X[col_name] = (X["language"] == val).astype(int)
            X = X.drop(columns=["language"])

        # 其他列 categorical -> 编码
        for col in X.columns:
            if X[col].dtype == object or str(X[col].dtype).startswith("category"):
                X[col] = pd.Categorical(X[col]).codes.astype("int64")
            
    y = df_design["accuracy"].values
    feature_names = list(X.columns) 

    # 4. permutation test with SHAP
    main_res, inter_res = permutation_test_shap(X, y, feature_names, n_perm=args.n_perm)

    # ==== 输出 ====
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 2000)
    print("\n==== 主效应结果排序 ====")
    print(main_res.sort_values(by=["p_value","importance_obs"], ascending=[True,False]))

    print("\n==== 交互效应结果排序 ====")
    print(inter_res.sort_values(by=["p_value","importance_obs"], ascending=[True,False]))

    combined = pd.concat([main_res, inter_res], ignore_index=True)
    combined_sorted = combined.sort_values(by=["p_value", "importance_obs"], ascending=[True, False])

    print("\n==== 主效应 + 交互效应混合排序 ====")
    print(combined_sorted)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="XGBoost + categorical 特征 + SHAP交互 + Permutation Test")
    parser.add_argument("--logfile", type=str, default="log/anova_kimiv1.log")
    parser.add_argument("--pkl_path", type=str, default="L36_design.pkl")
    parser.add_argument("--sample_num", type=int, default=36)
    parser.add_argument("--n_perm", type=int, default=200)
    parser.add_argument("--merge_language", action="store_true")
    args = parser.parse_args()
    main(args)