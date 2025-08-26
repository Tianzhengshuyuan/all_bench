import re
import pickle
import pandas as pd
import argparse
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols
import seaborn as sns
import matplotlib.pyplot as plt


pattern1 = re.compile(
    r"总题组数:\s*\d+.*?第一轮正确答案数:\s*\d+.*?正确率:\s*[\d.]+%.*?第二轮正确答案数:\s*\d+.*?正确率:\s*([\d.]+)%"
)
pattern2 = re.compile(
    r"总题数:\s*\d+.*?正确数:\s*\d+.*?正确率:\s*([\d.]+)%,\s*耗时:"
)

def get_accuracies(logfile, max_samples=None):
    accuracies = []
    with open(logfile, "r", encoding="utf-8") as f:
        for line in f:
            m1 = pattern1.search(line)
            if m1:
                acc = float(m1.group(1)) / 100.0
                accuracies.append(acc)
                if max_samples is not None and len(accuracies) >= max_samples:
                    break
                continue
            m2 = pattern2.search(line)
            if m2:
                acc = float(m2.group(1)) / 100.0
                accuracies.append(acc)
                if max_samples is not None and len(accuracies) >= max_samples:
                    break
    return np.array(accuracies)


# ===================== 主流程 =====================
def get_main_anova():
    # 1. 读取正交设计
    with open(args.pkl_path, "rb") as f:
        design_list = pickle.load(f)[: args.sample_num]
    df_design = pd.DataFrame(design_list)

    # 2. 读取准确率
    accuracies = get_accuracies(args.logfile, max_samples=args.sample_num)
    if len(accuracies) != args.sample_num:
        raise ValueError(f"预计{args.sample_num}个准确率，实际得到 {len(accuracies)} 个，请检查日志文件")

    df_design["accuracy"] = accuracies

    print("==== 前几行设计 + 准确率数据 ====")
    print(df_design.head(), "\n")

    # 3. ANOVA 分析
    # A:B表示 A 和 B 的交互效应（interaction only），不包含主效应
    # A*B表示 A + B + A:B
    formula = (
        "accuracy ~ C(language) + C(question_type) + C(question_tran) "
        "+ C(few) + C(cot) + C(mul) "
        "+ Temperature + max_tokens + top_p + presence_penalty"
    )
    # ols = Ordinary Least Squares（普通最小二乘回归）, .fit拟合模型，得到一个回归结果对象 model
    model = ols(formula, data=df_design).fit()
    # sm.stats.anova_lm基于回归结果做方差分析
    # Type I：按公式顺序依次分解，结果受变量顺序影响。
    # Type II：考虑主效应，不受变量顺序影响，但不考虑交互项。
    # Type III：考虑所有效应（包括交互），适合不平衡设计。
    anova_table = sm.stats.anova_lm(model, typ=3)
    # .drop("Residual")：删除残差行。
    # .sort_values(by="F", ascending=False)：按 F 值从大到小排序。
    anova_sorted = anova_table.drop("Residual").sort_values(by="F", ascending=False)

    print("==== ANOVA 分析结果 ====")
    print(anova_sorted, "\n")

    # 4. 可视化（举例：语言因子）
    sns.boxplot(x="language", y="accuracy", data=df_design)
    plt.title("Accuracy by Language")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("anova_language.png")
    print("✅ 箱线图已保存为 anova_language.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ANOVA 分析主程序")
    parser.add_argument("--logfile", type=str, default="log/anova_kimiv1.log", help="日志文件路径")
    parser.add_argument("--pkl_path", type=str, default="L36_design.pkl", help="正交设计 pkl 文件路径")
    parser.add_argument("--sample_num", type=int, default=36)
    args = parser.parse_args()
    get_main_anova()