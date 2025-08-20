import argparse
import numpy as np
import sys
import re
from scipy.stats import norm

# 编译两种正则
pattern1 = re.compile(
    r"总题组数:\s*\d+.*?第一轮正确答案数:\s*\d+.*?正确率:\s*[\d.]+%.*?第二轮正确答案数:\s*\d+.*?正确率:\s*([\d.]+)%"
)
pattern2 = re.compile(
    r"总题数:\s*\d+.*?正确数:\s*\d+.*?正确率:\s*([\d.]+)%,\s*耗时:"
)

def get_accuracies(logfile, max_samples=100):
    accuracies = []
    with open(logfile, 'r', encoding='utf-8') as f:
        for line in f:
            m1 = pattern1.search(line)
            if m1:
                acc = float(m1.group(1)) / 100.0
                accuracies.append(acc)
                if len(accuracies) >= max_samples:
                    break
                continue
            m2 = pattern2.search(line)
            if m2:
                acc = float(m2.group(1)) / 100.0
                accuracies.append(acc)
                if len(accuracies) >= max_samples:
                    break
    if len(accuracies) == 0:
        print("未能从日志文件中抽取到准确率数据，请检查日志内容和正则表达式。")
        sys.exit(1)
    return np.array(accuracies)

def get_z(confidence):
    # 置信度转z值
    return norm.ppf(1 - (1 - confidence) / 2)

def get_sample_num():
    sample_std = np.std(data, ddof=1)
    error = args.error
    confidence = args.confidence
    population = args.population

    z = get_z(confidence)

    n0 = (z ** 2) * (sample_std ** 2) / (error ** 2)
    n0 = int(np.ceil(n0))
    # 有限总体修正
    if population is not None and population > 0:
        n = n0 / (1 + (n0 - 1) / population)
        n = int(np.ceil(n))
        print(f"从日志采样到的准确率样本数量: {len(data)}")
        print(f"样本均值: {np.mean(data):.4f}")
        print(f"样本标准差: {sample_std:.4f}")
        print(f"初步估算样本量（无限总体）: {n0}")
        print(f"有限总体修正后样本量（总体N={population}）: {n}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="根据log文件中采样到的准确率，和误差/置信度，估算所需样本量")
    parser.add_argument("--log", default="log/sample_test.log", help="日志文件路径")
    parser.add_argument("--error", type=float, default="0.03", help="允许的最大误差（绝对值），如0.05")
    parser.add_argument("--confidence", type=float, default=0.95, help="置信水平，如0.95/0.99")
    parser.add_argument("--population", type=int, default=15552, help="总体大小（如15552），如不指定则不做有限总体修正")
    parser.add_argument("--max_samples", type=int, default=100, help="从日志文件采样的最大样本数")
    args = parser.parse_args()
    data = get_accuracies(args.log, max_samples=args.max_samples)
    get_sample_num()