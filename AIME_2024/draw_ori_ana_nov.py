import re
import argparse
import numpy as np
import os
import matplotlib.pyplot as plt

# 两种正则模式
pattern1 = re.compile(
    r"总题组数:\s*\d+.*?第一轮正确答案数:\s*\d+.*?正确率:\s*[\d.]+%.*?第二轮正确答案数:\s*\d+.*?正确率:\s*([\d.]+)%"
)
pattern2 = re.compile(
    r"总题数:\s*\d+.*?正确数:\s*\d+.*?正确率:\s*([\d.]+)%,\s*耗时:"
)

def extract_accuracy(logfile):
    """提取日志中的第一个准确率，尝试两种正则"""
    if not os.path.exists(logfile):
        return None
    with open(logfile, 'r', encoding='utf-8') as f:
        for line in f:
            m1 = pattern1.search(line)
            if m1:
                return float(m1.group(1)) / 100.0
            m2 = pattern2.search(line)
            if m2:
                return float(m2.group(1)) / 100.0
    return None

def prettify_labels(labels):
    mapping = {
        "deepseekv3": "deepseek-v3",
        "doubao": "doubao-1.5-pro-32k",
        "gpt35": "gpt-3.5",
        "gpt41": "gpt-4.1",
        "kimiv1": "moonshot-v1-8k",
        "mistralM": "mistral-medium",
        "mistralL": "mistral-large",
        "qwen": "qwen-plus",
        "qwen25": "qwen2.5-32b-instruct",
    }
    return [mapping.get(lbl, lbl) for lbl in labels]

def process_logs(input_folder):
    if args.cot:
        default_files = [
            f for f in os.listdir(input_folder)
            if f.startswith("default_cot_") and f.endswith(".log")
        ]
    else:
        default_files = [
            f for f in os.listdir(input_folder)
            if f.startswith("default_") and f.endswith(".log") and not f.startswith("default_cot_")
        ]
    if not default_files:
        print("未找到任何 default_*.log 文件！")
        exit()

    labels, default_accs, ana_accs, nov_accs = [], [], [], []

    for f in sorted(default_files):
        default_file = os.path.join(input_folder, f)
        if args.cot:
            label = f.replace("default_cot_", "").replace(".log", "")
            ana_file = os.path.join(input_folder, f"ana_cot_{label}.log")
        else:
            label = f.replace("default_", "").replace(".log", "")
            ana_file = os.path.join(input_folder, f"ana_{label}.log")
        nov_file = os.path.join(input_folder, f"nov_{label}.log")

        default_acc = extract_accuracy(default_file)
        ana_acc = extract_accuracy(ana_file)
        nov_acc = extract_accuracy(nov_file)

        if default_acc is not None or ana_acc is not None:
            labels.append(label)
            default_accs.append(default_acc)
            ana_accs.append(ana_acc)
            nov_accs.append(nov_acc)
    print(f"labels: {labels}")
    print(f"default_accs: {default_accs}"
              f", ana_accs: {ana_accs}"
              f", nov_accs: {nov_accs}")
    return labels, default_accs, ana_accs, nov_accs

def plot_results(labels, default_accs, ana_accs, nov_accs):
    x = np.arange(len(labels))
    width = 0.25   # 每组的宽度稍微窄一些，保证能放下三根柱子

    plt.figure(figsize=(9,6))
    bars1 = plt.bar(x - width, default_accs, width, label="Default", color="purple")
    bars2 = plt.bar(x, ana_accs, width, label="Analogical", color="green")
    # bars3 = plt.bar(x + width, nov_accs, width, label="Novel", color="orange")

    # 给每个 bar 添加数值标签
    def add_labels(bars):
        for bar in bars:
            height = bar.get_height()
            if height is not None:  # 可能有 None，需要判断
                plt.text(
                    bar.get_x() + bar.get_width() / 2,
                    height + 0.01,
                    f"{height:.2f}",
                    ha="center", va="bottom", fontsize=6
                )

    add_labels(bars1)
    add_labels(bars2)
    # add_labels(bars3)

    plt.xticks(x, prettify_labels(labels), fontsize=10, rotation=30, ha='right')
    plt.ylabel("Accuracy", fontsize=14)
    plt.xlabel("LLM", fontsize=14)
    plt.legend(fontsize=11)
    plt.tight_layout()
    if args.cot:
        plt.ylim(0, 0.8)
        plt.savefig("default_ana_nov_cot.png", dpi=300)
    else:
        plt.ylim(0, 0.5)  # 更宽泛的范围，避免数值显示被遮挡，可以按需求改
        plt.savefig("default_ana_nov.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="比较 default 和 analogical 的准确率")
    parser.add_argument("--input_folder", default="log", help="包含日志文件的文件夹")
    parser.add_argument("--cot", action="store_true", help="是否处理 CoT 日志文件")
    args = parser.parse_args()

    labels, default_accs, ana_accs, nov_accs = process_logs(args.input_folder)
    plot_results(labels, default_accs, ana_accs, nov_accs)