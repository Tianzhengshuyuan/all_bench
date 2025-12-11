import re
import os
import pickle
import pandas as pd
import argparse
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from tqdm import trange


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


def bootstrap_anova(df, formula, n_boot=500, alpha=0.05):
    """对每个因子做 bootstrap，返回均值+置信区间"""
    effects = {}

    for _ in trange(n_boot, desc="Bootstrap"):
        boot = df.sample(n=len(df), replace=True)
        model = ols(formula, data=boot).fit()
        anova_res = anova_lm(model, typ=2)

        # 保存 sum_sq
        for idx, row in anova_res.drop("Residual").iterrows():
            effects.setdefault(idx, []).append(row["sum_sq"])

    results = []
    for factor, values in effects.items():
        arr = np.array(values)
        lower = np.percentile(arr, 100*alpha/2)
        upper = np.percentile(arr, 100*(1-alpha/2))
        mean_val = arr.mean()
        sig = not (lower <= 0 <= upper)
        results.append({
            "factor": factor,
            "mean_sum_sq": mean_val,
            f"{100*(alpha/2):.1f}%": lower,
            f"{100*(1-alpha/2):.1f}%": upper,
            "significant": sig
        })
    return pd.DataFrame(results).sort_values(by="mean_sum_sq", ascending=False)

# ===================== Permutation Test =====================
def permutation_test_anova(df, formula, n_perm=500):
    """对每个因子做 permutation test，返回经验 p 值"""
    # 1. 原始 ANOVA 结果
    model = ols(formula, data=df).fit()
    anova_res = anova_lm(model, typ=2)
    obs_ss = anova_res["sum_sq"].drop("Residual")

    # 2. 置换分布
    null_distrib = {factor: [] for factor in obs_ss.index}
    acc = df["accuracy"].copy()

    for _ in trange(n_perm, desc="Permutation"):
        shuffled = df.copy()
        shuffled["accuracy"] = np.random.permutation(acc)
        model_perm = ols(formula, data=shuffled).fit()
        anova_perm = anova_lm(model_perm, typ=2)
        for factor in obs_ss.index:
            null_distrib[factor].append(anova_perm.loc[factor, "sum_sq"])

    # 3. 经验 p 值计算
    results = []
    for factor, ss in obs_ss.items():
        perm_vals = np.array(null_distrib[factor])
        p_value = np.mean(perm_vals >= ss)
        results.append({
            "factor": factor,
            "obs_sum_sq": ss,
            "perm_mean": perm_vals.mean(),
            "p_value": p_value
        })
    return pd.DataFrame(results).sort_values(by="p_value")

def permutation_test_anova_eta(df, formula, n_perm=500):
    """对每个因子做 permutation test，返回基于 η² 的经验 p 值"""
    # 1. 原始 ANOVA 结果
    model = ols(formula, data=df).fit()
    anova_res = anova_lm(model, typ=2)
    ss_total = anova_res["sum_sq"].sum()
    obs_eta = (anova_res["sum_sq"] / ss_total).drop("Residual")  # η²

    # 2. 置换分布
    null_distrib = {factor: [] for factor in obs_eta.index}
    acc = df["accuracy"].copy()

    for _ in trange(n_perm, desc="Permutation (eta²)"):
        shuffled = df.copy()
        shuffled["accuracy"] = np.random.permutation(acc)
        model_perm = ols(formula, data=shuffled).fit()
        anova_perm = anova_lm(model_perm, typ=2)
        ss_total_perm = anova_perm["sum_sq"].sum()
        for factor in obs_eta.index:
            eta_perm = anova_perm.loc[factor, "sum_sq"] / ss_total_perm
            null_distrib[factor].append(eta_perm)

    # 3. 经验 p 值
    results = []
    eta_sum = 0
    
    for factor, eta in obs_eta.items():
        eta_sum += eta
        perm_vals = np.array(null_distrib[factor])
        p_value = np.mean(perm_vals >= eta)
        results.append({
            "factor": factor,
            "obs_eta2": eta,      
            "perm_mean_eta2": perm_vals.mean(),
            "p_value": p_value
        })
    print(f"所有因子 η² 之和: {eta_sum:.4f}")
    return pd.DataFrame(results).sort_values(by="obs_eta2", ascending=False)

# ===================== 主流程 =====================
def get_main_anova():
    # 1. 读取正交设计
    with open(args.pkl_path, "rb") as f:
        design_list = pickle.load(f)[: args.sample_num]
    df_design = pd.DataFrame(design_list)

    # 2. 读取准确率
    accuracies = get_accuracies(args.logfile, max_samples=args.sample_num)
    if len(accuracies) != args.sample_num:
        raise ValueError(f"预计 {args.sample_num} 个准确率，实际得到 {len(accuracies)} 个，请检查日志文件")

    df_design["accuracy"] = accuracies

    # 3. 构造公式
    if args.merge_language:
        main_effects = [
            "C(language)", "C(question_type)", "C(question_tran)",
            "C(few)", "C(cot)", "C(mul)",
            "C(Temperature)", "C(max_tokens)", "C(top_p)", "C(presence_penalty)"
        ]
        # 构造交互项：所有两两组合
        interaction_terms = []
        for i in range(len(main_effects)):
            for j in range(i + 1, len(main_effects)):
                a, b = main_effects[i], main_effects[j]
                interaction_terms.append(f"{a}:{b}")
    else:
        # 拆分语言为哑变量
        languages = ["alby", "ey", "fy", "ry", "yy", "zw"]
        for lang in languages:
            df_design[f"lang_{lang}"] = (df_design["language"] == lang).astype(int)
        
        lang_vars = [f"C(lang_{lang})" for lang in languages]
        # other_vars = [
        #     "C(question_type)", "C(question_tran)",
        #     "C(few)", "C(cot)", "C(mul)",
        #     "Temperature", "max_tokens", "top_p", "presence_penalty"
        # ]
        other_vars = [
            "C(question_type)", "C(question_tran)",
            "C(few)", "C(cot)", "C(mul)",
            "C(Temperature)", "C(max_tokens)", "C(top_p)", "C(presence_penalty)"
        ]
       
        main_effects = lang_vars + other_vars

        # 构造交互项：所有两两组合，排除“语言 x 语言”
        interaction_terms = []
        for i in range(len(main_effects)):
            for j in range(i + 1, len(main_effects)):
                a, b = main_effects[i], main_effects[j]
                if a in lang_vars and b in lang_vars:  # 跳过语言-语言交互
                    continue
                interaction_terms.append(f"{a}:{b}")

    # 拼接公式
    if args.interaction:
        formula = "accuracy ~ " + " + ".join(main_effects + interaction_terms) 
    else:
        formula = "accuracy ~ " + " + ".join(main_effects) 
        
    # # 4. ANOVA 分析
    # model = ols(formula, data=df_design).fit()
    # anova_table = sm.stats.anova_lm(model, typ=3)
    # anova_sorted = anova_table.drop("Residual").sort_values(by="F", ascending=False)

    # # 5. 处理 p 值
    # raw_p_values = anova_sorted["PR(>F)"].astype(float).values
    # anova_sorted["PR(>F)"] = anova_sorted["PR(>F)"].apply(lambda x: f"{x:.10f}")

    # # 6. 插入分隔线
    # cutoff_idx = None
    # for i, p in enumerate(raw_p_values):
    #     if p > 0.05:
    #         cutoff_idx = i
    #         break
    # if cutoff_idx is not None:
    #     sep = pd.DataFrame([["-"*10]*anova_sorted.shape[1]],
    #                        columns=anova_sorted.columns,
    #                        index=["-----------"])
    #     top = anova_sorted.iloc[:cutoff_idx]
    #     bottom = anova_sorted.iloc[cutoff_idx:]
    #     anova_sorted = pd.concat([top, sep, bottom])

    # # 7. 打印结果
    # log_name = os.path.basename(args.logfile)
    # log_name = log_name.replace("anova_", "").replace(".log", "")
    # print(f"==== {log_name} ANOVA 分析结果 ====")
    pd.set_option("display.width", 2000)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    # print(anova_sorted, "\n")
    
    # 8. Bootstrap 结果
    # boot_res = bootstrap_anova(df_design, formula, n_boot=500)
    # print("\n==== Bootstrap 结果 (sum_sq CI) ====")
    # print(boot_res)

    # 9. Permutation Test 结果
    perm_res = permutation_test_anova_eta(df_design, formula, n_perm=500)
    print("\n==== Permutation Test 结果 (经验 p 值) ====")
    print(perm_res)

# ===================== 入口 =====================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ANOVA 分析主程序")
    parser.add_argument("--logfile", type=str, default="log/anova_kimiv1.log", help="日志文件路径")
    parser.add_argument("--pkl_path", type=str, default="L36_design.pkl", help="正交设计 pkl 文件路径")
    parser.add_argument("--sample_num", type=int, default=36)
    parser.add_argument("--merge_language", action="store_true", help="是否将语言作为单一因子处理")
    parser.add_argument("--interaction", action="store_true", help="是否包含交互项")
    args = parser.parse_args()
    get_main_anova()