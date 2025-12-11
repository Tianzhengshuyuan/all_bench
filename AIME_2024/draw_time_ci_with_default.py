import re
import argparse
import numpy as np
import os
from scipy import stats
import matplotlib.pyplot as plt

# 正则模式
pattern1 = re.compile(
    r"总题组数:\s*\d+.*?第一轮正确答案数:\s*\d+.*?正确率:\s*[\d.]+%.*?第二轮正确答案数:\s*\d+.*?正确率:\s*[\d.]+%.*?总耗时:\s*([\d.]+)秒"
)
pattern2 = re.compile(
    r"总题数:\s*\d+.*?正确数:\s*\d+.*?正确率:\s*[\d.]+%,\s*耗时:\s*([\d.]+)s"
)

def get_latency(logfile, max_samples=100):
    times = []
    with open(logfile, 'r', encoding='utf-8') as f:
        for line in f:
            m1 = pattern1.search(line)
            if m1:
                time = float(m1.group(1)) 
                times.append(time)
                if len(times) >= max_samples:
                    break
                continue
            m2 = pattern2.search(line)
            if m2:
                time = float(m2.group(1)) 
                times.append(time)
                if len(times) >= max_samples:
                    break
    return np.array(times)

def get_default_accuracy(input_folder, label):
    """读取 default_{label}.log 并用 pattern2 匹配一个准确率"""
    default_file = os.path.join(input_folder, f"default_{label}.log")
    if not os.path.exists(default_file):
        return None
    with open(default_file, 'r', encoding='utf-8') as f:
        for line in f:
            m = pattern2.search(line)
            if m:
                return float(m.group(1)) 
    return None

def ci_normal(times, N, conf_level):
    n = len(times)
    mean = np.mean(times)
    std = np.std(times, ddof=1)
    se = std / np.sqrt(n)
    fpc = np.sqrt((N - n) / (N - 1))
    se_fpc = se * fpc
    t_value = stats.t.ppf(1 - (1 - conf_level) / 2, df=n-1)
    ci_lower = mean - t_value * se_fpc
    ci_upper = mean + t_value * se_fpc
    return mean, ci_lower, ci_upper

def ci_bootstrap(times, N, conf_level, n_boot=10000, random_seed=42):
    rng = np.random.default_rng(random_seed)
    n = len(times)
    means = []
    for _ in range(n_boot):
        sample = rng.choice(times, size=n, replace=True)
        means.append(np.mean(sample))
    alpha = 1 - conf_level
    lower_percentile = 100 * (alpha / 2)
    upper_percentile = 100 * (1 - alpha / 2)
    ci_lower = np.percentile(means, lower_percentile)
    ci_upper = np.percentile(means, upper_percentile)
    mean = np.mean(times)
    return mean, ci_lower, ci_upper

def extract_label_from_filename(filename):
    basename = os.path.basename(filename)
    # e.g. sample_test_deepseek.log -> deepseek
    return basename.replace("sample_test_", "").replace(".log", "")

def process_logs(input_folder, N, max_samples=100, method="normal", conf_levels=[0.95, 0.99]):
    log_files = [
        os.path.join(input_folder, f)
        for f in os.listdir(input_folder)
        if f.startswith("sample_test") and f.endswith(".log")
    ]
    if not log_files:
        print("未找到任何符合条件的log文件！")
        exit()

    labels, means, default_times = [], [], []
    ci_dict = {cl: {"lowers": [], "uppers": []} for cl in conf_levels}

    for log in sorted(log_files):
        times = get_latency(log, max_samples)
        if len(times) == 0:
            print(f"{log} 未提取到数据，跳过。")
            continue
        label = extract_label_from_filename(log)
        # 计算多个置信区间
        for cl in conf_levels:
            if method == "normal":
                mean, ci_lower, ci_upper = ci_normal(times, N, cl)
            elif method == "bootstrap":
                mean, ci_lower, ci_upper = ci_bootstrap(times, N, cl)
            else:
                raise ValueError("未知method参数，仅支持normal或bootstrap")
            if cl == conf_levels[0]:  # 只在第一次保存 mean 和 label
                labels.append(label)
                means.append(mean)
                # 读取 default_{label}.log 的准确率
                default_acc = get_default_accuracy(input_folder, label)
                default_times.append(default_acc)
            ci_dict[cl]["lowers"].append(ci_lower)
            ci_dict[cl]["uppers"].append(ci_upper)

    return labels, np.array(means), ci_dict, default_times

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
        # 可以在这里继续扩展其他映射
    }
    return [mapping.get(lbl, lbl) for lbl in labels]


def plot_results(labels, means, ci_dict, default_times):
    x = np.arange(len(labels))
    plt.figure(figsize=(8,6))

    # 不同置信区间的颜色
    colors = {0.95: "blue", 0.99: "orange"}

    for cl, vals in ci_dict.items():
        lowers = np.array(vals["lowers"])
        uppers = np.array(vals["uppers"])
        yerr = np.array([means - lowers, uppers - means])
        plt.errorbar(x, means, yerr=yerr, fmt='none', color=colors.get(cl, "gray"),
                     label=f'{int(cl*100)}% Confidence Intervals',
                     capsize=6, elinewidth=2, markersize=6)

    # 均值点
    plt.scatter(x, means, color='gray', s=50, zorder=5, label='Mean')

    # 默认准确率红叉
    for i, time in enumerate(default_times):
        if time is not None:
            plt.scatter(x[i], time, color='#eeafaf', s=50, label='Default' if i == 0 else "")

    plt.xticks(x, prettify_labels(labels), fontsize=10, rotation=20, ha='right')
    plt.ylabel('Latency', fontsize=14)
    plt.xlabel('LLM', fontsize=14)
    # plt.title('Latency and Confidence Intervals for LLMs', fontsize=15, weight='bold')
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig('llm_latency_ci.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="从日志文件中提取时间并绘制多个置信区间图")
    parser.add_argument('--input_folder', default="log", help="包含日志文件的文件夹")
    parser.add_argument('--N', type=int, default=15552, help="配置空间大小")
    parser.add_argument('--max_samples', type=int, default=500, help="采样样本数")
    parser.add_argument('--method', default="normal", choices=["normal", "bootstrap"], help="计算方法: normal或bootstrap")
    args = parser.parse_args()

    # 同时计算 95% 和 99% 置信区间
    conf_levels = [0.95, 0.99]
    labels, means, ci_dict, default_times = process_logs(args.input_folder, args.N, args.max_samples, args.method, conf_levels)
    plot_results(labels, means, ci_dict, default_times)