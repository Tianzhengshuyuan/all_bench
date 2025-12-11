import argparse
import numpy as np
import sys
import re
from scipy.stats import norm

# ======================
# 正则匹配日志中的准确率
# ======================
pattern1 = re.compile(
    r"总题组数:\s*\d+.*?第一轮正确答案数:\s*\d+.*?正确率:\s*[\d.]+%.*?第二轮正确答案数:\s*\d+.*?正确率:\s*([\d.]+)%"
)
pattern2 = re.compile(
    r"总题数:\s*\d+.*?正确数:\s*\d+.*?正确率:\s*([\d.]+)%,\s*耗时:"
)

def get_accuracies(logfile, start=0, max_samples=100):
    """
    从日志文件中获取准确率数据 (0~1)
    """
    accuracies = []
    with open(logfile, 'r', encoding='utf-8') as f:
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

    if len(accuracies) == 0:
        print("❌ 未能从日志文件中抽取到准确率数据，请检查日志内容和正则表达式。")
        sys.exit(1)

    if start >= len(accuracies):
        print(f"❌ 指定的起始样本 {start} 超出日志中样本数量 {len(accuracies)}")
        sys.exit(1)

    selected = accuracies[start:start + max_samples]
    return np.array(selected)

# ======================
# 顺序采样方法
# ======================
def get_z(confidence):
    """置信度转 z 值"""
    return norm.ppf(1 - (1 - confidence) / 2)

def sequential_analysis(data, error=0.03, confidence=0.95, batch_size=20, min_samples=50):
    """
    顺序分析 (Sequential Sampling)
    data: 准确率样本 (array, 每个元素 ∈ [0,1])
    error: 允许的最大误差 (置信区间半宽)
    confidence: 置信水平
    batch_size: 每次增加的样本数
    min_samples: 至少采样的最小样本数
    """
    z = get_z(confidence)
    n_total = len(data)

    for n in range(min_samples, n_total + 1, batch_size):
        sample = data[:n]
        mean = np.mean(sample)
        std = np.std(sample, ddof=1)
        se = std / np.sqrt(n)  # 标准误
        margin = z * se
        ci_low, ci_high = mean - margin, mean + margin

        print(f"样本数: {n}, 均值: {mean:.4f}, CI: [{ci_low:.4f}, {ci_high:.4f}], 区间宽度: {2*margin:.4f}")

        # 判断是否满足精度要求
        if margin <= error:
            print(f"\n✅ 在样本数 {n} 时提前停止，置信区间半宽 {margin:.4f} ≤ 误差阈值 {error}")
            return n, mean, (ci_low, ci_high)

    # 如果数据用完仍不满足要求
    print(f"\n⚠️ 数据用尽({n_total} 个样本)，仍未达到误差阈值 {error}")
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    se = std / np.sqrt(n_total)
    margin = z * se
    return n_total, mean, (mean - margin, mean + margin)

# ======================
# 主程序入口
# ======================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="顺序分析 (Sequential Sampling)，基于日志中抽取的准确率")
    parser.add_argument("--log", default="log/sample_test.log", help="日志文件路径")
    parser.add_argument("--error", type=float, default=0.03, help="允许的最大误差 (置信区间半宽，如0.03)")
    parser.add_argument("--confidence", type=float, default=0.95, help="置信水平 (如0.95/0.99)")
    parser.add_argument("--batch_size", type=int, default=20, help="每次增加的样本数")
    parser.add_argument("--min_samples", type=int, default=50, help="至少采样的最小样本数")
    parser.add_argument("--max_samples", type=int, default=500, help="最多使用多少个样本")
    parser.add_argument("--start", type=int, default=0, help="从第几个样本开始取数据 (0 表示第一个样本)")
    args = parser.parse_args()

    # 读取日志中的准确率
    data = get_accuracies(args.log, args.start, max_samples=args.max_samples)

    # 顺序分析
    sequential_analysis(data, error=args.error, confidence=args.confidence,
                        batch_size=args.batch_size, min_samples=args.min_samples)