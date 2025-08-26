import os
import re
import pickle
import pandas as pd
import argparse
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols
import seaborn as sns
import matplotlib.pyplot as plt

# ============ 正则模式 ============
pattern1 = re.compile(
    r"总题组数:\s*\d+.*?第一轮正确答案数:\s*\d+.*?正确率:\s*[\d.]+%.*?第二轮正确答案数:\s*\d+.*?正确率:\s*([\d.]+)%"
)
pattern2 = re.compile(
    r"总题数:\s*\d+.*?正确数:\s*\d+.*?正确率:\s*([\d.]+)%,\s*耗时:"
)

def get_accuracies(logfile):
    """从单个日志文件中提取准确率"""
    accuracies = []
    with open(logfile, "r", encoding="utf-8") as f:
        for line in f:
            m1 = pattern1.search(line)
            if m1:
                acc = float(m1.group(1)) / 100.0
                accuracies.append(acc)
                continue
            m2 = pattern2.search(line)
            if m2:
                acc = float(m2.group(1)) / 100.0
                accuracies.append(acc)
    return np.array(accuracies)


def run_anova_for_file(logfile, design_list):
    """对单个日志文件运行 ANOVA，返回结果表"""
    accuracies = get_accuracies(logfile)
    n = len(accuracies)
    if n == 0:
        print(f"⚠️ {logfile} 没有提取到准确率，跳过")
        return None

    if len(design_list) < n:
        print(f"⚠️ {logfile} 样本数 {n} 超过设计数 {len(design_list)}，截断")
        n = len(design_list)
        accuracies = accuracies[:n]

    df_design = pd.DataFrame(design_list[:n])
    df_design["accuracy"] = accuracies

    formula = (
        "accuracy ~ C(language) + C(question_type) + C(question_tran) "
        "+ C(few) + C(cot) + C(mul) "
        "+ Temperature + max_tokens + top_p + presence_penalty"
    )
    model = ols(formula, data=df_design).fit()
    anova_table = sm.stats.anova_lm(model, typ=3)
    anova_sorted = anova_table.drop("Residual")
    print(f"\n==== ANOVA 结果: {os.path.basename(logfile)} ====")
    print(anova_sorted.sort_values(by="F", ascending=False))
    return anova_sorted, df_design


def get_main_anova():
    # 1. 读取正交设计
    with open(args.pkl_path, "rb") as f:
        design_list = pickle.load(f)

    # 2. 遍历所有 sample_test*.log 文件
    all_tables = []
    first_df = None
    for fname in os.listdir(args.input_folder):
        if not fname.startswith("sample_test_") or not fname.endswith(".log"):
            continue
        logfile = os.path.join(args.input_folder, fname)
        print(f"📂 处理日志文件: {fname}")
        result = run_anova_for_file(logfile, design_list)
        if result is not None:
            anova_table, df_design = result
            anova_table["logfile"] = fname
            all_tables.append(anova_table)
            if first_df is None:
                first_df = df_design  # 保存第一个文件的数据用于画图

    if not all_tables:
        print("❌ 没有有效的 ANOVA 结果")
        return

    # 3. 汇总结果
    combined = pd.concat(all_tables)
    summary = combined.groupby(combined.index).agg({"F": "mean", "PR(>F)": "mean"}).sort_values(by="F", ascending=False)

    print("\n==== 综合 ANOVA 结果（平均 F 值和 P 值） ====")
    print(summary)

    # 4. 可视化（示例：语言）
    if first_df is not None:
        sns.boxplot(x="language", y="accuracy", data=first_df)
        plt.title("Accuracy by Language (example from first log)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("anova_language.png")
        print("✅ 箱线图已保存为 anova_language.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="多文件 ANOVA 分析程序")
    parser.add_argument("--input_folder", type=str, default="log", help="日志文件目录")
    parser.add_argument("--pkl_path", type=str, default="sample_data_v1.2.pkl", help="正交设计 pkl 文件路径")
    args = parser.parse_args()
    get_main_anova()