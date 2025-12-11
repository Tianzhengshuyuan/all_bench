import argparse
import numpy as np
import sys
import re
import os
import matplotlib.pyplot as plt
from scipy.stats import norm, t

# 编译两种正则
pattern1 = re.compile(
    r"总题组数:\s*\d+.*?第一轮正确答案数:\s*\d+.*?正确率:\s*[\d.]+%.*?第二轮正确答案数:\s*\d+.*?正确率:\s*([\d.]+)%"
)
pattern2 = re.compile(
    r"总题数:\s*\d+.*?正确数:\s*\d+.*?正确率:\s*([\d.]+)%,\s*耗时:"
)

config_pattern_default = re.compile(r"配置 key=(\d+),\s*配置=.*")

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

    if start >= len(accuracies):
        print(f"指定的起始样本 {start} 超出日志中样本数量 {len(accuracies)}")
        sys.exit(1)

    selected = accuracies[start:start + max_samples]
    
    # # 散点图
    # accuracies_arrays = np.array(accuracies)
    # plt.figure(figsize=(10, 5))
    # plt.scatter(range(1, len(accuracies_arrays) + 1), accuracies_arrays, alpha=0.6, s=20, c="blue", label="accuracy")
    # plt.axhline(np.mean(accuracies_arrays), color="red", linestyle="--", label=f"mean {np.mean(accuracies_arrays):.4f}")
    # plt.xlabel("samples")
    # plt.ylabel("accuracy")
    # plt.title("accuracy scatter plot")
    # plt.legend()
    # plt.tight_layout()
    # plt.savefig("accuracy_scatter_plot.png")
    
    return np.array(selected)

def get_key_accuracies(logfile, folder_name):
    config_pattern = config_pattern_default

    key_acc_map = {}
    current_key = None

    with open(logfile, "r", encoding="utf-8") as f:
        for line in f:
            # 匹配配置行，更新当前 key
            m_cfg = config_pattern.search(line)
            if m_cfg:
                current_key = int(m_cfg.group(1))
                continue

            # 匹配 accuracy
            m1 = pattern1.search(line)
            m2 = pattern2.search(line)
            acc = None
            if m1:
                acc = float(m1.group(1)) / 100.0
            elif m2:
                acc = float(m2.group(1)) / 100.0

            # 记录当前 key 的 accuracy（1 次）
            if acc is not None and current_key is not None:
                if current_key not in key_acc_map:
                    key_acc_map[current_key] = acc
                # 用完一个 key 就清空，避免把后续行也归到同一个 key
                current_key = None

    return key_acc_map

def collect_dir_data(dir_path, label, max_samples=100):
    """
    从目录 dir_path 中所有包含 label 且以 sample_test_ 开头、.log 结尾的文件里，
    收集 key=0..max_samples-1 的 accuracy，返回一个按 key 排序的 numpy 数组。
    """
    if not os.path.isdir(dir_path):
        print(f"[ERROR] 目录 {dir_path} 不存在或不是目录。")
        sys.exit(1)

    print(f"[INFO] 从目录 {dir_path} 中收集 label={label} 的日志数据 ...")
    all_files = [
        f for f in os.listdir(dir_path)
        if f.startswith(f"sample_test_{label}_") and f.endswith(".log")
    ]
    if not all_files:
        print(f"[ERROR] 目录 {dir_path} 中未找到包含 label '{label}' 的 sample_test_*.log 文件。")
        sys.exit(1)

    merged = {}  # key -> accuracy
    for fname in all_files:
        path = os.path.join(dir_path, fname)
        try:
            key_acc_map = get_key_accuracies(path, os.path.basename(dir_path))
            for k, v in key_acc_map.items():
                # 若同一 key 在多个文件出现，只保留第一次，可按需改为平均
                if k not in merged:
                    merged[k] = v
        except Exception as e:
            print(f"[ERROR] 文件 {path} 解析失败: {e}")

    # 只取 0 ~ max_samples-1
    keys = sorted(k for k in merged.keys() if 0 <= k < max_samples)
    if not keys:
        print(f"[ERROR] 在目录 {dir_path} 中未找到 key 范围在 [0, {max_samples}) 的配置。")
        sys.exit(1)

    # 按 key 顺序生成 accuracy 数组
    accuracies = np.array([merged[k] for k in keys])
    print(f"[INFO] 收集到 {len(accuracies)} 个有效样本（不同 key）。")
    # 简单缺失检查
    expected = set(range(min(keys), max_samples))
    missing = sorted(expected - set(keys))
    if missing:
        print(
            f"[WARN] 缺少 {len(missing)} 个 key "
            f"(例如 {missing[:15]}{'...' if len(missing) > 15 else ''})"
        )
    else:
        print(f"[OK] key 0–{max_samples-1} 全部存在。")

    return accuracies

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
        var_est = bootstrap_var(data, n_boot=2000, q=100)
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

# ========== 新增：收敛检测 ==========

def mean_ci_t(data, confidence=0.95):
    """基于 student-t 分布计算均值和置信区间"""
    n = len(data)
    mean = np.mean(data)
    se = np.std(data, ddof=1) / np.sqrt(n)
    h = se * t.ppf((1 + confidence) / 2., n - 1)
    return mean, (mean - h, mean + h)

def check_convergence(data, confidence=0.95, step=10, tol_mean=0.002, tol_ci=0.06, consecutive=3):
    """
    动态检测均值和置信区间是否收敛
    """
    history = []
    stable_count = 0

    for n in range(step, len(data) + 1, step):
        subset = data[:n]
        mean, ci = mean_ci_t(subset, confidence)
        ci_width = ci[1] - ci[0]
        history.append((n, mean, ci, ci_width))


        if len(history) > 1:
            prev_mean = history[-2][1]
            if abs(mean - prev_mean) < tol_mean and ci_width < tol_ci:
                stable_count += 1
                print("find stable")
                if stable_count >= consecutive:
                    print(f"\n✅ 收敛: 样本量需求约 {n}")
                    plot_convergence(history)
                    return n, history
            else:
                stable_count = 0
            print(f"样本数 {n}: 均值={mean:.4f}, 均值差={abs(mean-prev_mean):.5f}, 95%CI={ci}, CI宽度={ci_width:.4f}")

    print("\n⚠ 未达到收敛条件，请考虑更多样本")
    plot_convergence(history)
    return None, history

def plot_convergence(history):
    """绘制均值和置信区间收敛曲线"""
    ns = [h[0] for h in history]
    means = [h[1] for h in history]
    ci_lows = [h[2][0] for h in history]
    ci_highs = [h[2][1] for h in history]

    plt.figure(figsize=(10, 6))
    plt.plot(ns, means, label="mean", color="blue")
    plt.fill_between(ns, ci_lows, ci_highs, color="blue", alpha=0.2, label="95% CI")
    plt.xlabel("Sample size")
    plt.ylabel("Accuracy")
    plt.title("Convergence of mean and confidence interval")
    plt.legend()
    plt.tight_layout()
    plt.savefig("convergence_plot.png")
    print("已保存收敛曲线: convergence_plot.png")

# ========== 主程序 ==========

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="根据log文件中采样到的准确率，和误差/置信度，估算所需样本量")
    parser.add_argument("--log", default="log/sample_test.log", help="日志文件路径")
    parser.add_argument("--dir", default=None, help="日志文件所在的文件夹；若设置，则从目录中汇总 key→accuracy 数据")
    parser.add_argument("--label", default="doubao", help="在 --dir 模式下，用于筛选文件名中包含的模型标签")
    parser.add_argument("--error", type=float, default=0.06, help="允许的最大误差（绝对值），如0.05")
    parser.add_argument("--confidence", type=float, default=0.95, help="置信水平，如0.95/0.99")
    parser.add_argument("--population", type=int, default=15552, help="总体大小，如不指定则不做有限总体修正")
    parser.add_argument("--max_samples", type=int, default=500, help="从日志文件采样的最大样本数")
    parser.add_argument("--start", type=int, default=0, help="从第几个样本开始取数据（0表示第一个样本）")
    args = parser.parse_args()

    if args.dir is not None:
        # 目录 + label + key 模式
        data = collect_dir_data(args.dir, args.label, max_samples=args.max_samples)
    else:
        # 单文件 + 顺序行模式（原逻辑）
        data = get_accuracies(args.log, args.start, max_samples=args.max_samples)
    # data = get_accuracies(args.log, args.start, max_samples=args.max_samples)

    # 三种方法
    get_sample_num(method="pilot")
    get_sample_num(method="max")
    get_sample_num(method="bootstrap")

    # 收敛检测
    check_convergence(data, confidence=args.confidence, step=10, tol_mean=0.003, tol_ci=args.error)