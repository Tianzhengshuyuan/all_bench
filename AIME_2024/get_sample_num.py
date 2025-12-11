import argparse
import numpy as np
import sys
import re
import matplotlib.pyplot as plt
from scipy.stats import norm

# 编译两种正则
pattern1 = re.compile(
    r"总题组数:\s*\d+.*?第一轮正确答案数:\s*\d+.*?正确率:\s*[\d.]+%.*?第二轮正确答案数:\s*\d+.*?正确率:\s*([\d.]+)%"
)
pattern2 = re.compile(
    r"总题数:\s*\d+.*?正确数:\s*\d+.*?正确率:\s*([\d.]+)%,\s*耗时:"
)

def get_accuracies(logfile, start=0, max_samples=100):
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
        print("未能从日志文件中抽取到准确率数据，请检查日志内容和正则表达式。")
        sys.exit(1)
    print(f"从日志文件中抽取到 {len(accuracies)} 个样本的准确率数据。")
    # count = 0
    # summary = 0.0
    # print("前100个样本的准确率:")
    # for i in range(100):
    #     if accuracies[i]:
    #         count += 1
    #         summary += accuracies[i]
    #         print(f"样本 {i+1}: {accuracies[i]:.4f}")
    # print(f"共计 {count} 个非0样本, 平均准确率 {summary/100}")
    # count = 0
    # summary = 0.0
    # print("第100-200 个样本的准确率:")
    # for i in range(100, 200):
    #     if accuracies[i]:
    #         count += 1
    #         summary += accuracies[i]
    #         print(f"样本 {i+1}: {accuracies[i]:.4f}")
    # print(f"共计 {count} 个非0样本, 平均准确率 {summary/100}")
    # count = 0
    # summary = 0.0
    # print("第200-300 个样本的准确率:")
    # for i in range(200, 300):
    #     if accuracies[i]:
    #         count += 1
    #         summary += accuracies[i]
    #         print(f"样本 {i+1}: {accuracies[i]:.4f}")
    # print(f"共计 {count} 个非0样本, 平均准确率 {summary/100}")
    # count = 0
    # summary = 0.0
    # print("第300-400 个样本的准确率:")  
    # for i in range(300, 400):
    #     if accuracies[i]:
    #         count += 1
    #         summary += accuracies[i]
    #         print(f"样本 {i+1}: {accuracies[i]:.4f}")
    # print(f"共计 {count} 个非0样本, 平均准确率 {summary/100}")
    # count = 0
    # summary = 0.0
    # print("第400-500 个样本的准确率:")  
    # for i in range(400, 500):
    #     if accuracies[i]:
    #         count += 1
    #         summary += accuracies[i]
    #         print(f"样本 {i+1}: {accuracies[i]:.4f}")
    # print(f"共计 {count} 个非0样本, 平均准确率 {summary/100}")

    if start >= len(accuracies):
        print(f"指定的起始样本 {start} 超出日志中样本数量 {len(accuracies)}")
        sys.exit(1)

    selected = accuracies[start:start + max_samples]
    accuracies_arrays = np.array(accuracies)
    
    plt.figure(figsize=(10, 5))
    plt.scatter(range(1, len(accuracies_arrays) + 1), accuracies_arrays, alpha=0.6, s=20, c="blue", label="accuracy")
    plt.axhline(np.mean(accuracies_arrays), color="red", linestyle="--", label=f"mean {np.mean(accuracies_arrays):.4f}")
    plt.xlabel("samples")
    plt.ylabel("accuracy")
    plt.title("accuracy scatter plot")
    plt.legend()
    plt.tight_layout()
    plt.savefig("accuracy_scatter_plot.png")
    
    return np.array(selected)

def get_z(confidence):
    return norm.ppf(1 - (1 - confidence) / 2)

def bootstrap_var(data, n_boot=1000, seed=42, q=95):
    rng = np.random.default_rng(seed)
    boot_vars = []
    n = len(data)
    for _ in range(n_boot):
        sample = rng.choice(data, size=n, replace=True)
        boot_vars.append(np.var(sample, ddof=1))
    return np.percentile(boot_vars, q)

def get_sample_num(method="pilot"):
    """
    method:
      - "pilot": 使用pilot样本方差
      - "max": 使用二项分布最大方差近似 (0.25)
      - "bootstrap": 使用bootstrap方差上限
    """
    error = args.error
    confidence = args.confidence
    population = args.population
    z = get_z(confidence)

    if method == "pilot":
        var_est = np.var(data, ddof=1)
        desc = "pilot 样本方差"
    elif method == "max":
        var_est = 0.25  # 最大可能方差
        desc = "二项分布最大方差近似 (0.25)"
    elif method == "bootstrap":
        var_est = bootstrap_var(data, n_boot=2000, q=100)  # 取95%分位数
        desc = "bootstrap 方差上限"
    else:
        raise ValueError("method 必须是 'pilot' / 'max' / 'bootstrap'")

    n0 = (z ** 2) * var_est / (error ** 2)
    n0 = int(np.ceil(n0))

    if population is not None and population > 0:
        n = n0 / (1 + (n0 - 1) / population)
        n = int(np.ceil(n))
    else:
        n = n0

    print(f"方法: {desc}")
    print(f"从日志采样到的准确率样本数量: {len(data)}")
    print(f"样本均值: {np.mean(data):.4f}")
    print(f"估计方差: {var_est:.4f}")
    print(f"初步估算样本量（无限总体）: {n0}")
    print(f"有限总体修正后样本量（总体N={population}）: {n}")
    print("-" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="根据log文件中采样到的准确率，和误差/置信度，估算所需样本量")
    parser.add_argument("--log", default="log/sample_test.log", help="日志文件路径")
    parser.add_argument("--error", type=float, default=0.03, help="允许的最大误差（绝对值），如0.05")
    parser.add_argument("--confidence", type=float, default=0.95, help="置信水平，如0.95/0.99")
    parser.add_argument("--population", type=int, default=15552, help="总体大小（如15552），如不指定则不做有限总体修正")
    parser.add_argument("--max_samples", type=int, default=100, help="从日志文件采样的最大样本数")
    parser.add_argument("--start", type=int, default=0, help="从第几个样本开始取数据（0表示第一个样本）")
    args = parser.parse_args()

    data = get_accuracies(args.log, args.start, max_samples=args.max_samples)

    # 三种方法都输出，便于比较
    get_sample_num(method="pilot")
    get_sample_num(method="max")
    get_sample_num(method="bootstrap")