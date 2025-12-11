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
    "gpt41": 48.1 / 100.0,
    "kimik2": 69.6 / 100.0,
    "qwen3": 32.8 / 100.0,
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

def prettify_labels(labels):
    mapping = {
        "deepseekv3": "deepseek-v3",
        "doubao": "doubao-1.5-pro",
        "gpt35": "gpt-3.5",
        "gpt41": "gpt-4.1",
        "kimiv1": "moonshot-v1-8k",
        "mistralL": "mistral-large",
        "mistralM": "mistral-medium",
        "qwen": "qwen-plus",
        "qwen25": "qwen2.5-32b",
        # 可以在这里继续扩展其他映射
    }
    return [mapping.get(lbl, lbl) for lbl in labels]

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
            # accuracies = (accuracies - base) / base  # 相对变化率
            accuracies = (accuracies - base)   # 变化量

        labels.append(label)
        data.append(accuracies)

    if not data:
        print("没有数据可绘制。")
        return

    # 绘制箱线图
    plt.figure(figsize=(10, 6))
    if args.diff:
        plt.boxplot(data, labels=labels, patch_artist=True, boxprops=dict(facecolor="orange"), medianprops=dict(color="#519aba"))
        plt.ylabel("Relative Deviation from Reported Accuracy", fontsize=18)
        # plt.title(f"Deviation of Measured Accuracy from Reported Accuracy on {args.model}",fontsize=18)
        # 标出中位数
        medians = []
        for i, accuracies in enumerate(data, start=1):
            median_val = np.median(accuracies)
            medians.append(median_val)
            plt.text(
                i+0.35, median_val-0.02,
                f"{median_val:.2f}",
                color="#519aba",
                ha="center",
                va="bottom",
                fontsize=12
            )
        # 添加 legend 
        median_line = plt.Line2D([], [], color="#519aba", label="Median line")
        plt.legend(handles=[median_line], fontsize=12, loc="best")
    else:
        plt.boxplot(data, labels=labels, patch_artist=True)
        plt.ylabel("Accuracy", fontsize=18)
        # plt.title(f"Distribution of Model Accuracies on {args.model}")
        
        # 用绿色水平线标注 BASE_ACCURACIES
        # for i, label in enumerate(labels, start=1):
        #     if label in BASE_ACCURACIES:
        #         base = BASE_ACCURACIES[label]
        #         # 在箱线图对应位置画水平线
        #         plt.hlines(base, i - 0.3, i + 0.3, colors="lightgreen", linestyles="--", linewidth=2,
        #                    label="Baseline" if i == 1 else "")
        #         # 标注数值
        #         plt.text(i + 0.35, base, f"{base:.2f}", color="green", fontsize=9, va="center")
        
    plt.xlabel("LLM", fontsize=20)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()
    if args.diff:
        plt.savefig(f"relative_change_{args.output}", dpi=300)
        print(f"箱线图已保存到relative_change_{args.output}")
    else:
        plt.savefig(args.output, dpi=300)
        print(f"箱线图已保存到 {args.output}")
        
def get_bar():
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

        # 提取标签
        label = filename.replace("related_work_", "").replace(".log", "")
        if label not in BASE_ACCURACIES:
            continue

        if args.diff:
            base = BASE_ACCURACIES[label]
            accuracies = (accuracies - base)   # 相对变化量

        labels.append(label)
        data.append(accuracies)

    if not data:
        print("没有数据可绘制。")
        return

    # 计算统计指标
    means = [np.mean(d) for d in data]
    medians = [np.median(d) for d in data]
    mins = [np.min(d) for d in data]
    maxs = [np.max(d) for d in data]

    x = np.arange(len(labels))
    box_width = 0.5  # 箱体宽度

    plt.figure(figsize=(10, 6))

    for i in range(len(labels)):
        # 绘制箱体 (min–max)
        plt.bar(
            x[i],
            maxs[i] - mins[i],  # 高度
            bottom=mins[i],     # 起点
            width=box_width,
            color="#9975a6",
            edgecolor="black",
            alpha=0.7
        )

        # 均值线
        plt.hlines(means[i], x[i] - box_width/2, x[i] + box_width/2,
                   colors="purple", lw=2, label="Mean" if i == 0 else "")

        # 中位数线
        plt.hlines(medians[i], x[i] - box_width/2, x[i] + box_width/2,
                   colors="#519aba", lw=2, label="Median" if i == 0 else "")

    plt.xticks(x, labels, fontsize=18)
    if args.diff:
        plt.ylabel("Deviation from Reported Accuracy", fontsize=18)
    else:
        plt.ylabel("Accuracy", fontsize=18)
    plt.xlabel("LLM", fontsize=20)
    plt.yticks(fontsize=18)
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.legend(fontsize=14)
    plt.tight_layout()

    if args.diff:
        output_file = f"relative_change_bar_{args.output}"
    else:
        output_file = f"bar_{args.output}"
    plt.savefig(output_file, dpi=300)
    plt.show()
    print(f"箱体条形图已保存到 {output_file}")
    
def get_violin():
    # 遍历文件夹，找到所有相关文件
    files = [
        f for f in os.listdir(args.input_folder)
        if f.startswith("sample_test_") and f.endswith(".log")
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
        label = filename.replace("sample_test_", "").replace(".log", "")
        print(f"label: {label}")
        # if label not in BASE_ACCURACIES:
        #     continue

        if args.diff:
            base = BASE_ACCURACIES[label]
            accuracies = (accuracies - base)   # 差值模式

        labels.append(label)
        data.append(accuracies)

    if not data:
        print("没有数据可绘制。")
        return

    # 绘制小提琴图
    plt.figure(figsize=(10, 6))
    parts = plt.violinplot(
        data,
        widths=0.6,
        showmeans=True,    # 显示均值
        showmedians=True,  # 显示中位数
        showextrema=True   # 显示最大最小
    )
    parts['cmeans'].set_color("#ea6864")
    parts['cmedians'].set_color("#519aba")
    parts['cmaxes'].set_color("#555555")
    parts['cmins'].set_color("#555555")
    parts['cbars'].set_color("#555555")

    # 设置颜色
    for pc in parts['bodies']:
        pc.set_facecolor("#9975a6")
        pc.set_alpha(0.7)

    # 用水平线标注 BASE_ACCURACIES
    # for i, label in enumerate(labels, start=1):
    #     if label in BASE_ACCURACIES:
    #         base = BASE_ACCURACIES[label]
    #         # 在箱线图对应位置画水平线
    #         plt.hlines(base, i - 0.15, i + 0.15, colors="#ffa500", linestyles="--", linewidth=2,
    #                     label="Baseline" if i == 1 else "")
    #         # 标注数值
    #         plt.text(i - 0.4, base, f"{base:.2f}", color="#d95c26", fontsize=11, va="center")
            
    mean_handle = plt.Line2D([0], [0], color="#ea6864", lw=2, label="Mean")
    median_handle = plt.Line2D([0], [0], color="#519aba", lw=2, label="Median")
    report_handle = plt.Line2D([0], [0], color="#ffa500", lw=2, linestyle="--", label="Reported Accuracy")  
    plt.legend(handles=[mean_handle, median_handle, report_handle], fontsize=14)
    
    plt.xticks(np.arange(1, len(labels)+1), prettify_labels(labels), fontsize=15, rotation=30, ha="right")
    if args.diff:
        plt.ylabel("Deviation from Reported Accuracy", fontsize=18)
    else:
        plt.ylabel("Accuracy", fontsize=18)
    plt.xlabel("LLM", fontsize=20)
    plt.yticks(fontsize=18)
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()

    if args.diff:
        output_file = f"relative_change_violin_{args.output}"
    else:
        output_file = f"violin_{args.output}"
    plt.savefig(output_file, dpi=300)
    plt.show()
    print(f"小提琴图已保存到 {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="提取准确率并绘制箱线图")
    parser.add_argument("--input_folder", default="log", help="包含 related_work*.log 文件的文件夹路径")
    parser.add_argument("--max_samples", type=int, default=None, help="每个文件最多提取的样本数")
    parser.add_argument("--output", default="boxplot.png", help="输出图像文件名 (默认: boxplot.png)")
    parser.add_argument("--diff", action="store_true", help="是否绘制相对原始accuracy的变化率 (默认: False)")
    parser.add_argument("--model", default="AIME")
    args = parser.parse_args()
    # get_box()
    # # get_bar()
    get_violin()
    