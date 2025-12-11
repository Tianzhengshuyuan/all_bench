import re
import os
import pandas as pd
import matplotlib.pyplot as plt

# 正则模式
pattern1 = re.compile(
    r"总题组数:\s*\d+.*?第一轮正确答案数:\s*\d+.*?正确率:\s*[\d.]+%.*?第二轮正确答案数:\s*\d+.*?正确率:\s*([\d.]+)%"
)
pattern2 = re.compile(
    r"总题数:\s*\d+.*?正确数:\s*\d+.*?正确率:\s*([\d.]+)%,\s*耗时:"
)
pattern_config = re.compile(
    r"配置: {(.*?)}"
)

LANGUAGE_COLORS = {
    "yy": "red",
    "zw": "blue",
    "ry": "green",
    "ey": "orange",
    "fy": "purple",
    "alby": "brown"
}

def parse_log_files(folder, label):
    """解析某个label的所有日志 -> DataFrame"""
    records = []
    for fname in os.listdir(folder):
        # print("fname=", fname)
        # print(f"sample_test_{label}.log")
        if fname == f"sample_test_{label}.log":
            print("find!!")
            fpath = os.path.join(folder, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                lines = f.readlines()
            config = None
            for line in lines:
                m_cfg = pattern_config.search(line)
                if m_cfg:
                    config_str = m_cfg.group(1)
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
                        row["LLMs"] = label  # 增加 LLMs 字段
                        records.append(row)
                        config = None
    return pd.DataFrame(records)


def plot_scatter_by_language(df, label):
    """每个 label 单独画散点图"""
    if df.empty:
        print(f"[INFO] {label} 没有数据，跳过")
        return
    
    # ===== 打印均值 =====
    means = df.groupby("language")["accuracy"].mean()
    print(f"\n== {label} ==\n{means.round(4)}\n")
    
    plt.figure(figsize=(6,6))
    for lang in df["language"].unique():
        sub = df[df["language"] == lang]
        plt.scatter(
            [lang]*len(sub), sub["accuracy"],
            color=LANGUAGE_COLORS.get(lang, "gray"),
            alpha=0.7, label=lang if lang not in plt.gca().get_legend_handles_labels()[1] else ""
        )
    plt.title(f"Accuracy distribution of {label}", fontsize=14, weight="bold")
    plt.ylabel("Accuracy")
    plt.xlabel("Language")
    plt.ylim(0,1.0)
    plt.legend(title="Language")
    plt.tight_layout()
    plt.savefig(f"{label}_scatter.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_folder", default="log", help="日志目录")
    parser.add_argument("--labels", nargs="+", required=True, help="要处理的label，比如 deepseekv3 gpt41")
    args = parser.parse_args()

    for label in args.labels:
        df = parse_log_files(args.input_folder, label)
        plot_scatter_by_language(df, label)