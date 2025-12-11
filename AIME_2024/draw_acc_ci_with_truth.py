import re
import argparse
import numpy as np
import os
from scipy import stats
import matplotlib.pyplot as plt

# 正则模式
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
    # print(accuracies)
        if "mistralL" in logfile:
            plt.figure(figsize=(8, 4))
            plt.scatter(range(len(accuracies)), accuracies, c='blue', alpha=0.7)
            plt.title("Accuracies from Log File")
            plt.xlabel("Sample Index")
            plt.ylabel("Accuracy")
            plt.ylim(0,0.8)
            plt.xlim(0,144)
            plt.grid(True, linestyle="--", alpha=0.6)
            plt.tight_layout()
            plt.savefig("sample_accuracy.png", dpi=300)  # 保存为PNG文件
    return np.array(accuracies)

def get_anova_all_accuracy(label):
    """从 anova_all 文件夹中读取与 label 匹配的所有日志，提取准确率并计算均值"""
    folder = "anova_all"
    if not os.path.exists(folder):
        return None
    max_samples = 1000
    accuracies = []
    for fname in os.listdir(folder):
        if label not in fname:
            continue
        filepath = os.path.join(folder, fname)
        with open(filepath, 'r', encoding='utf-8') as f:
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
        return None

    print(f"Found {len(accuracies)} accuracies for label {label} in anova_all.")
    return float(np.mean(accuracies))

def ci_normal(accuracies, N, conf_level):
    n = len(accuracies)
    mean = np.mean(accuracies)
    std = np.std(accuracies, ddof=1)
    se = std / np.sqrt(n)
    fpc = np.sqrt((N - n) / (N - 1))
    se_fpc = se * fpc
    t_value = stats.t.ppf(1 - (1 - conf_level) / 2, df=n-1)
    ci_lower = mean - t_value * se_fpc
    ci_upper = mean + t_value * se_fpc
    return mean, ci_lower, ci_upper

def ci_bootstrap(accuracies, N, conf_level, n_boot=10000, random_seed=42):
    rng = np.random.default_rng(random_seed)
    n = len(accuracies)
    means = []
    for _ in range(n_boot):
        sample = rng.choice(accuracies, size=n, replace=True)
        means.append(np.mean(sample))
    alpha = 1 - conf_level
    lower_percentile = 100 * (alpha / 2)
    upper_percentile = 100 * (1 - alpha / 2)
    ci_lower = np.percentile(means, lower_percentile)
    ci_upper = np.percentile(means, upper_percentile)
    mean = np.mean(accuracies)
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

    labels, means, anova_all_accs = [], [], []
    ci_dict = {cl: {"lowers": [], "uppers": []} for cl in conf_levels}

    for log in sorted(log_files):
        accuracies = get_accuracies(log, max_samples)
        if len(accuracies) == 0:
            print(f"{log} 未提取到数据，跳过。")
            continue
        label = extract_label_from_filename(log)
        # 计算多个置信区间
        for cl in conf_levels:
            if method == "normal":
                mean, ci_lower, ci_upper = ci_normal(accuracies, N, cl)
            elif method == "bootstrap":
                mean, ci_lower, ci_upper = ci_bootstrap(accuracies, N, cl)
            else:
                raise ValueError("未知method参数，仅支持normal或bootstrap")
            if cl == conf_levels[0]:  # 只在第一次保存 mean 和 label
                labels.append(label)
                means.append(mean)
                # 读取 default_{label}.log 的准确率
                anova_all_acc = get_anova_all_accuracy(label)
                anova_all_accs.append(anova_all_acc)
            ci_dict[cl]["lowers"].append(ci_lower)
            ci_dict[cl]["uppers"].append(ci_upper)

    return labels, np.array(means), ci_dict, anova_all_accs

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

def plot_results(labels, means, ci_dict, anova_all_accs):
    x = np.arange(len(labels))
    plt.figure(figsize=(8,6))

    # 不同置信区间的颜色
    colors = {0.95: "blue", 0.99: "orange"}

    for cl, vals in ci_dict.items():
        lowers = np.array(vals["lowers"])
        print("Lowers:", lowers)
        uppers = np.array(vals["uppers"])
        yerr = np.array([means - lowers, uppers - means])
        plt.errorbar(x, means, yerr=yerr, fmt='none', color=colors.get(cl, "gray"),
                     label=f'{int(cl*100)}% Confidence Intervals',
                     capsize=6, elinewidth=2, markersize=6)

    # 均值点
    plt.scatter(x, means, color='green', s=50, zorder=5, label='Mean')
    print(labels, means)

    # ground truth准确率红叉
    for i, acc in enumerate(anova_all_accs):
        if acc is not None:
            plt.scatter(x[i], acc, color='purple', s=50, label='Ground Truth' if i == 0 else "")
            print(f"Ground Truth for {labels[i]}: {acc:.4f}")

    plt.xticks(x, prettify_labels(labels), fontsize=10, rotation=20, ha='right')
    plt.ylabel('Accuracy', fontsize=14)
    plt.xlabel('LLM', fontsize=14)
    # plt.title('Accuracy and Confidence Intervals for LLMs', fontsize=15, weight='bold')
    plt.ylim(0, 0.3)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig('llm_accuracy_ci_with_truth.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="从日志文件中提取准确率并绘制多个置信区间图")
    parser.add_argument('--input_folder', default="log", help="包含日志文件的文件夹")
    parser.add_argument('--N', type=int, default=15552, help="配置空间大小")
    parser.add_argument('--max_samples', type=int, default=500, help="采样样本数")
    parser.add_argument('--method', default="normal", choices=["normal", "bootstrap"], help="计算方法: normal或bootstrap")
    args = parser.parse_args()

    # 同时计算 95% 和 99% 置信区间
    conf_levels = [0.95, 0.99]
    labels, means, ci_dict, anova_all_accs = process_logs(args.input_folder, args.N, args.max_samples, args.method, conf_levels)
    plot_results(labels, means, ci_dict, anova_all_accs)