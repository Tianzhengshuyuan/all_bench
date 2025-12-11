import re
import argparse
import numpy as np
import os
from scipy import stats
import matplotlib.pyplot as plt
import itertools

# 正则模式
pattern1 = re.compile(
    r"总题组数:\s*\d+.*?第一轮正确答案数:\s*\d+.*?正确率:\s*[\d.]+%.*?第二轮正确答案数:\s*\d+.*?正确率:\s*([\d.]+)%"
)
pattern2 = re.compile(
    r"总题数:\s*\d+.*?正确数:\s*\d+.*?正确率:\s*([\d.]+)%,\s*耗时:"
)
pattern_key = re.compile(r"处理key:\s*(\d+),\s*配置:")

LABEL_MAX_SAMPLES = {
    "gpt41": 260,
    "gpt35": 220,
    "mistralM": 260,
    "mistralL": 290,
    "qwen": 260,       # qwen-plus
    "qwen25": 400,     # qwen2.5
    "deepseekv3": 320, # deepseek3
    "doubao": 480,
    "kimiv1": 220        # kimiv1
}
def get_config_accuracies(logfile, max_samples=1000):
    """返回 {config_key: acc}"""
    config_accs = {}
    current_key = None
    with open(logfile, 'r', encoding='utf-8') as f:
        for line in f:
            mk = pattern_key.search(line)
            if mk:
                current_key = int(mk.group(1))
                continue
            if current_key is not None:
                m1 = pattern1.search(line)
                if m1:
                    acc = float(m1.group(1)) / 100.0
                    config_accs[current_key] = acc
                    current_key = None
                else:
                    m2 = pattern2.search(line)
                    if m2:
                        acc = float(m2.group(1)) / 100.0
                        config_accs[current_key] = acc
                        current_key = None
    # 限制样本数
    if len(config_accs) > max_samples:
        config_accs = dict(list(config_accs.items())[:max_samples])
    return config_accs

def get_default_accuracy(input_folder, label):
    """读取 default_{label}.log 并用 pattern2 匹配一个准确率"""
    default_file = os.path.join(input_folder, f"default_{label}.log")
    if not os.path.exists(default_file):
        return None
    with open(default_file, 'r', encoding='utf-8') as f:
        for line in f:
            m = pattern2.search(line)
            if m:
                return float(m.group(1)) / 100.0
    return None

def ci_bootstrap(data, conf_level, n_boot=10000, random_seed=42):
    rng = np.random.default_rng(random_seed)
    n = len(data)
    means = []
    for _ in range(n_boot):
        sample = rng.choice(data, size=n, replace=True)
        means.append(np.mean(sample))
    alpha = 1 - conf_level
    lower = np.percentile(means, 100*alpha/2)
    upper = np.percentile(means, 100*(1-alpha/2))
    return np.mean(data), lower, upper

def extract_label_from_filename(filename):
    basename = os.path.basename(filename)
    return basename.replace("sample_test_", "").replace(".log", "")

def prettify_labels(labels):
    mapping = {
        "deepseekv3": "deepseek-v3",
        "doubao": "doubao-1.5-pro",
        "gpt35": "gpt3.5",
        "gpt41": "gpt4.1",
        "kimiv1": "moonshot-v1",
        "mistralM": "mistral-m",
        "mistralL": "mistral-l",
        "qwen": "qwen-plus",
        "qwen25": "qwen2.5",
    }
    pretty = []
    for lbl in labels:
        if "-" in lbl:  # a-b 对比
            a, b = lbl.split("-", 1)
            a_pretty = mapping.get(a, a)
            b_pretty = mapping.get(b, b)
            pretty.append(f"{a_pretty} " + r"$\mathbf{-}$" + f" {b_pretty}")
        else:  # 单个名字
            pretty.append(mapping.get(lbl, lbl))
    return pretty

def process_differences(input_folder, max_samples=1000, conf_levels=[0.95, 0.99]):
    # 读取所有模型的 {config_id: acc}
    log_files = [
        os.path.join(input_folder, f)
        for f in os.listdir(input_folder)
        if f.startswith("sample_test") and f.endswith(".log")
    ]
    if not log_files:
        print("未找到任何符合条件的log文件！")
        exit()

    results = {}   # label → {config_id: acc}
    defaults = {}
    labels = []

    for log in sorted(log_files):
        label = extract_label_from_filename(log)
        labels.append(label)
        results[label] = get_config_accuracies(log, max_samples)
        defaults[label] = get_default_accuracy(input_folder, label)

    # 两两比较
    pair_labels, mean_diffs, ci_dict, default_diffs = [], [], {cl: {"lowers":[], "uppers":[]} for cl in conf_levels}, []
    for a, b in itertools.combinations(labels, 2):
        # 对齐配置
        common_keys = set(results[a].keys()) & set(results[b].keys())
        if not common_keys:
            continue
        diffs = [results[a][k] - results[b][k] for k in common_keys]
        # CI
        mdiffs, lowers, uppers = {}, {}, {}
        for cl in conf_levels:
            mean, lo, up = ci_bootstrap(diffs, cl)
            mdiffs[cl] = mean
            lowers[cl] = lo
            uppers[cl] = up
        # 保存
        pair_labels.append(f"{a}-{b}")
        mean_diffs.append(mdiffs[conf_levels[0]])  # 取95%时的mean
        for cl in conf_levels:
            ci_dict[cl]["lowers"].append(lowers[cl])
            ci_dict[cl]["uppers"].append(uppers[cl])
        # default 差
        if defaults[a] is not None and defaults[b] is not None:
            default_diffs.append(defaults[a] - defaults[b])
        else:
            default_diffs.append(None)

    return pair_labels, np.array(mean_diffs), ci_dict, default_diffs

def plot_differences(pair_labels, mean_diffs, ci_dict, default_diffs):
    x = np.arange(len(pair_labels))
    plt.figure(figsize=(10,6))

    colors = {0.95:"blue", 0.99:"orange"}

    for cl, vals in ci_dict.items():
        lowers = np.array(vals["lowers"])
        uppers = np.array(vals["uppers"])
        yerr = np.array([mean_diffs - lowers, uppers - mean_diffs])
        plt.errorbar(x, mean_diffs, yerr=yerr, fmt='o', color=colors.get(cl,"gray"),
                     label=f"{int(cl*100)}% CI", capsize=5)

    # 均值点 
    plt.scatter(x, mean_diffs, color='green', s=40, label='Mean', zorder=5)

    # 默认值差异 
    for i, d in enumerate(default_diffs):
        if d is not None:
            plt.scatter(x[i], d, color='purple', s=40, label='Default' if i==0 else "")

    plt.axhline(0, color='gray', linestyle='--')
    plt.xticks(x, prettify_labels(pair_labels), fontsize=8, rotation=30, ha='right')
    plt.ylabel("Accuracy Difference", fontsize=10)
    # plt.title("Distribution of Performance Differences Across Models", fontsize=15, weight='bold')
    plt.legend()
    plt.tight_layout()
    plt.savefig("llm_accuracy_diff2.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="比较不同模型之间配置准确率的差异及置信区间")
    parser.add_argument('--input_folder', default="ames_result_origin", help="包含日志文件的文件夹")
    parser.add_argument('--max_samples', type=int, default=500, help="采样样本数")
    args = parser.parse_args()

    conf_levels = [0.95, 0.99]
    pair_labels, mean_diffs, ci_dict, default_diffs = process_differences(
        args.input_folder, args.max_samples, conf_levels
    )
    plot_differences(pair_labels, mean_diffs, ci_dict, default_diffs)