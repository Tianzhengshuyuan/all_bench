import os
import re
import argparse
import numpy as np
import matplotlib.pyplot as plt

# 正则模式
pattern1 = re.compile(
    r"总题组数:\s*\d+.*?第一轮正确答案数:\s*\d+.*?正确率:\s*[\d.]+%.*?第二轮正确答案数:\s*\d+.*?正确率:\s*([\d.]+)%"
)
pattern2 = re.compile(
    r"总题数:\s*\d+.*?正确数:\s*\d+.*?正确率:\s*([\d.]+)%,\s*耗时:"
)

# 四个基准 accuracy
BASE_ACCURACIES = {
    "deepseekv3": 39.2 / 100.0,
    "gpt4.1": 69.6 / 100.0,
    "kimik2": 32.8 / 100.0,
    "qwen3": 48.1 / 100.0,
}

def get_accuracies(logfile, max_samples=None):
    accuracies = []
    with open(logfile, 'r', encoding='utf-8') as f:
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

def get_box():
    # 遍历文件夹，找到所有相关文件
    files = [
        f for f in os.listdir(args.input_folder)
        if f.startswith("related_work_") and f.endswith(".log")
    ]
    if not files:
        print("未找到符合条件的日志文件！")
        return

    labels = []
    data = []

    for filename in sorted(files):
        filepath = os.path.join(args.input_folder, filename)
        accuracies = get_accuracies(filepath, max_samples=args.max_samples)
        if len(accuracies) == 0:
            print(f"文件 {filename} 中未找到准确率数据，跳过。")
            continue

        # 提取横坐标标签
        label = filename.replace("related_work_", "").replace(".log", "")
        # 只考虑指定的 label
        if label not in BASE_ACCURACIES:
            continue

        if args.diff:
            base = BASE_ACCURACIES[label]
            accuracies = (accuracies - base) / base  # 相对变化率

        labels.append(label)
        data.append(accuracies)

    if not data:
        print("没有数据可绘制。")
        return

    # 绘制箱线图
    plt.figure(figsize=(10, 6))
    if args.diff:
        plt.boxplot(data, labels=labels, patch_artist=True, boxprops=dict(facecolor="orange"), medianprops=dict(color="red"))
        plt.ylabel("Relative Change in Accuracy")
        plt.title("Relative Accuracy Change Distribution on AIME")
    else:
        plt.boxplot(data, labels=labels, patch_artist=True)
        plt.ylabel("Accuracy")
        plt.title("Distribution of Model Accuracies on AIME")
        
        # 用绿色水平线标注 BASE_ACCURACIES
        for i, label in enumerate(labels, start=1):
            if label in BASE_ACCURACIES:
                base = BASE_ACCURACIES[label]
                # 在箱线图对应位置画水平线
                plt.hlines(base, i - 0.3, i + 0.3, colors="lightgreen", linestyles="--", linewidth=2,
                           label="Baseline" if i == 1 else "")
                # 标注数值
                plt.text(i + 0.35, base, f"{base:.2f}", color="green", fontsize=9, va="center")
    plt.xlabel("LLM")
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()
    if args.diff:
        plt.savefig(f"relative_change_{args.output}", dpi=300)
        print(f"箱线图已保存到relative_change_{args.output}")
    else:
        plt.savefig(args.output, dpi=300)
        print(f"箱线图已保存到 {args.output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="提取准确率并绘制箱线图")
    parser.add_argument("--input_folder", default="log", help="包含 related_work*.log 文件的文件夹路径")
    parser.add_argument("--max_samples", type=int, default=None, help="每个文件最多提取的样本数")
    parser.add_argument("--output", default="boxplot.png", help="输出图像文件名 (默认: boxplot.png)")
    parser.add_argument("--diff", action="store_true", help="是否绘制相对原始accuracy的变化率 (默认: False)")
    args = parser.parse_args()
    get_box()