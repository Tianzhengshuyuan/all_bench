import re
import os
import pandas as pd
import argparse
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from tqdm import trange
from scipy.stats import f

# ===================== 日志解析正则 =====================
pattern1 = re.compile(
    r"总题组数:\s*\d+.*?第一轮正确答案数:\s*\d+.*?正确率:\s*[\d.]+%.*?第二轮正确答案数:\s*\d+.*?正确率:\s*([\d.]+)%"
)
pattern2 = re.compile(
    r"总题数:\s*\d+.*?正确数:\s*\d+.*?正确率:\s*([\d.]+)%,\s*耗时:"
)
pattern_config = re.compile(
    r"配置 key=(\d+), 配置={(.*?)}"
)

# ===================== 因子名称映射 =====================
factor_name_map = {
    "C(question_type)": "Question Format",
    "C(cot)": "COT",
    "C(max_tokens)": "max_tokens",
    "C(Temperature)": "temperature",
    "C(presence_penalty)": "presence_penalty",
    "C(top_p)": "top_p",
    "C(language)": "Language",
    "C(question_tran)": "Question Paraphrase",
    "C(few)": "Shot",
    "C(mul)": "Multi Turn",
    "C(LLMs)": "LLMs"
}
def pretty_factor_name(factor: str) -> str:
    parts = factor.split(":")
    new_parts = []
    for p in parts:
        new_parts.append(factor_name_map.get(p, p))
    return "-".join(new_parts)

# ===================== 解析日志 =====================
def parse_log_files(folder, label):
    records = []
    for fname in os.listdir(folder):
        if fname.startswith(f"sample_test_{label}_"):
            fpath = os.path.join(folder, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                lines = f.readlines()
            config = None
            for line in lines:
                m_cfg = pattern_config.search(line)
                if m_cfg:
                    config_str = m_cfg.group(2)
                    try:
                        config_dict = eval("{" + config_str + "}")
                    except Exception as e:
                        print(f"[WARNING] 配置解析失败: {config_str}, 错误={e}")
                        config_dict = None
                    config = config_dict
                    continue
                if config is not None:
                    m1 = pattern1.search(line)
                    m2 = pattern2.search(line)
                    acc = None
                    if m1:
                        acc = float(m1.group(1)) / 100.0
                    elif m2:
                        acc = float(m2.group(1)) / 100.0
                    if acc is not None:
                        row = dict(config)
                        row["accuracy"] = acc
                        row["LLMs"] = label  # 增加一列 LLMs
                        records.append(row)
                        config = None
    return pd.DataFrame(records)

# ===================== Permutation Test =====================
def permutation_test_anova_eta(df, formula, n_perm=500):
    model = ols(formula, data=df).fit()
    anova_res = anova_lm(model, typ=2)
    ss_total = anova_res["sum_sq"].sum()
    obs_eta = (anova_res["sum_sq"] / ss_total).drop("Residual")

    null_distrib = {factor: [] for factor in obs_eta.index}
    acc = df["accuracy"].copy()

    for _ in trange(n_perm, desc="Permutation (eta²)", leave=False):
        shuffled = df.copy()
        shuffled["accuracy"] = np.random.permutation(acc)
        model_perm = ols(formula, data=shuffled).fit()
        anova_perm = anova_lm(model_perm, typ=2)
        ss_total_perm = anova_perm["sum_sq"].sum()
        for factor in obs_eta.index:
            eta_perm = anova_perm.loc[factor, "sum_sq"] / ss_total_perm
            null_distrib[factor].append(eta_perm)

    results = []
    for factor, eta in obs_eta.items():
        perm_vals = np.array(null_distrib[factor])
        p_value = np.mean(perm_vals >= eta)
        results.append({
            "factor": factor,
            "obs_eta2": eta,
            "perm_mean_eta2": perm_vals.mean(),
            "p_value": p_value
        })
    return pd.DataFrame(results).sort_values(by="obs_eta2", ascending=False)

# ===================== 单个 label 流程 =====================
def run_anova_for_label(folder, label, n_perm=500, interaction=False, outdir="anova_1024_result"):
    df_design = parse_log_files(folder, label)
    if len(df_design) == 0:
        print(f"[WARNING] Label={label} 没有解析到任何记录")
        return
    
    main_effects = [
        "C(language)", "C(question_type)", "C(question_tran)",
        "C(few)", "C(cot)", "C(mul)",
        "C(Temperature)", "C(max_tokens)", "C(top_p)", "C(presence_penalty)"
    ]
    if interaction:
        interaction_terms = [f"{a}:{b}" for i,a in enumerate(main_effects) for b in main_effects[i+1:]]
        formula = "accuracy ~ " + " + ".join(main_effects + interaction_terms) 
    else:
        formula = "accuracy ~ " + " + ".join(main_effects)

    # --- 运行置换检验 ---
    perm_res = permutation_test_anova_eta(df_design, formula, n_perm=n_perm)

    # --- 美化因子名 ---
    perm_res["factor"] = perm_res["factor"].apply(pretty_factor_name)

    # --- 加总 obs_eta ---
    obs_eta_sum = perm_res["obs_eta2"].sum()
    # 累计和 (running sum)
    perm_res["cum_eta2"] = perm_res["obs_eta2"].cumsum()
    # 累计比例
    perm_res["cum_ratio"] = perm_res["cum_eta2"] / obs_eta_sum

    # --- 输出文件 ---
    os.makedirs(outdir, exist_ok=True)
    out_path = os.path.join(outdir, f"{label}.log")
    with open(out_path, "w", encoding="utf-8") as fout:
        fout.write(f"==== Permutation Test ANOVA 结果 ({label}) ====\n")
        fout.write(f"总效应量 obs_eta_sum = {obs_eta_sum:.6f}\n\n")
        fout.write(perm_res.to_string(index=False))
    print(f"[INFO] {label} 结果已保存到 {out_path}")

# ===================== 多 label 一起 (LLMs 因素) =====================
def run_anova_vs_llms(folder, outdir="anova_1024_result"):
    label_list = ["deepseekv3", "kimiv1", "doubao", "qwen25", "qwen" "mistralM", "mistralL", "gpt35", "gpt41"]

    dfs = []
    for label in label_list:
        df_label = parse_log_files(folder, label)
        if len(df_label) > 0:
            dfs.append(df_label)
    if not dfs:
        print("[WARNING] 没有解析到任何数据")
        return
    df_all = pd.concat(dfs, ignore_index=True)

    factors = [
        "C(language)", "C(question_type)", "C(question_tran)",
        "C(few)", "C(cot)", "C(mul)",
        "C(Temperature)", "C(max_tokens)", "C(top_p)", "C(presence_penalty)",
        "C(LLMs)"
    ]
    formula = "accuracy ~ " + " + ".join(factors)

    model = ols(formula, data=df_all).fit()
    anova_res = anova_lm(model, typ=2)
    ss_total = anova_res["sum_sq"].sum()

    ms_llms = anova_res.loc["C(LLMs)", "sum_sq"] / anova_res.loc["C(LLMs)", "df"]
    df_llms = anova_res.loc["C(LLMs)", "df"]
    print(f"df_llm={df_llms}")

    results = []
    alpha = 0.05
    for factor, row in anova_res.drop("Residual").iterrows():
        ss = row["sum_sq"]
        df_factor = row["df"]
        ms_factor = ss / df_factor
        print(f"df_factor ({factor}) = {df_factor}")

        if factor == "C(LLMs)":
            f_compute = None
            f_table_val = None
            sig = None
        else:
            f_compute = ms_factor / ms_llms
            f_table_val = f.ppf(1 - alpha, df_factor, df_llms)
            sig = f_compute > f_table_val

        contrib = ss / ss_total
        results.append({
            "factor": pretty_factor_name(factor),
            "SS": ss,
            "contrib": f"{contrib*100:.2f}%",
            "F_compute": f_compute,
            "F_table": f_table_val,
            "significant": sig
        })
    df_out = pd.DataFrame(results)

    os.makedirs(outdir, exist_ok=True)
    out_path = os.path.join(outdir, "anova_vs_llms.csv")
    df_out.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"[INFO] LLMs 相对 ANOVA 结果已保存到 {out_path}")

# ===================== 入口 =====================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ANOVA 主程序 (逐 label + LLMs)")
    parser.add_argument("--folder", type=str, default="anova_all2", help="日志文件夹路径")
    parser.add_argument("--interaction", action="store_true", help="是否包含交互项")
    parser.add_argument("--n_perm", type=int, default=500, help="置换次数")
    args = parser.parse_args()

    label_list = ["deepseekv3", "kimiv1", "doubao", "qwen25", "qwen", "mistralM", "mistralL", "gpt35", "gpt41"]
    pd.set_option("display.width", 2000)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option("display.float_format", lambda x: f"{x:.6f}")  # 保留6位小数

    for label in label_list:
        run_anova_for_label(args.folder, label,
                            n_perm=args.n_perm,
                            interaction=args.interaction,
                            outdir="anova_1024_result2")

    run_anova_vs_llms(args.folder, outdir="anova_1024_result2")