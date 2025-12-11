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
pattern_key = re.compile(r"处理配置 key=\s*(\d+),\s*配置=")

LABEL_MAX_SAMPLES = {
    "gpt41": 260,
    "gpt35": 220,
    "mistralM": 260,
    "mistralL": 290,
    "qwen": 260,       # qwen-plus
    "qwen25": 400,     # qwen2.5
    "deepseekv3": 320, # deepseek3
    "doubao": 480,
    "kimiv1": 220      # kimiv1
}

# 固定要处理的 9 个 label
FIXED_LABELS = ["deepseekv3", "doubao", "gpt35", "gpt41", "kimiv1", "mistralL", "mistralM", "qwen", "qwen25"]

def get_config_accuracies_single_file(logfile, max_samples=1000):
    """读取单个 logfile，返回 {config_key: acc}"""
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
    # 限制样本数（对单文件的粗截断）
    if len(config_accs) > max_samples:
        config_accs = dict(list(config_accs.items())[:max_samples])
    return config_accs

def get_config_accuracies_multi_files(log_files, max_samples_per_label=1000):
    """
    支持同一 label 多个文件：
    输入：该 label 对应的多个 log_files 列表
    输出：合并后的 {config_key: acc}
    合并策略：同一个 key 只保留第一次出现的 accuracy
    """
    all_acc_map = {}
    for logfile in sorted(log_files):
        file_acc_map = get_config_accuracies_single_file(
            logfile,
            max_samples=max_samples_per_label
        )
        for k, v in file_acc_map.items():
            if k not in all_acc_map:   # 不覆盖已有 key
                all_acc_map[k] = v

    # 再整体按 key 排序后，根据 label 的最大样本数进行截断
    if len(all_acc_map) == 0:
        return {}

    sorted_keys = sorted(all_acc_map.keys())
    truncated_keys = sorted_keys[:max_samples_per_label]
    merged = {k: all_acc_map[k] for k in truncated_keys}
    return merged

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
    lower = np.percentile(means, 100 * alpha / 2)
    upper = np.percentile(means, 100 * (1 - alpha / 2))
    return np.mean(data), lower, upper

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
    """
    固定处理 FIXED_LABELS 中的 9 个 label。
    对于每个 label：
        - 搜索 input_folder 下所有文件名中包含 `_{label}_` 且以 `.log` 结尾的日志
        - 合并这些日志中的 {config_id: acc}
    然后两两 label 做差，计算 bootstrap CI。
    """
    # 先收集目录中的 .log 文件，供后面按 label 过滤
    all_log_files = [
        os.path.join(input_folder, f)
        for f in os.listdir(input_folder)
        if f.endswith(".log")
    ]
    if not all_log_files:
        print("未找到任何log文件！")
        exit()

    results = {}   # label → {config_id: acc}
    defaults = {}
    labels = []

    for label in FIXED_LABELS:
        # 为该 label 找到所有相关日志：文件名中包含 `_{label}_`
        label_files = [
            path for path in all_log_files
            if f"_{label}_" in os.path.basename(path)
            and os.path.basename(path).endswith(".log")
            and not os.path.basename(path).startswith("default_")
        ]
        if not label_files:
            print(f"警告: 未找到 label={label} 对应的日志文件")
            continue

        label_max = LABEL_MAX_SAMPLES.get(label, max_samples)
        acc_map = get_config_accuracies_multi_files(
            label_files,
            max_samples_per_label=label_max
        )
        if not acc_map:
            print(f"警告: label={label} 无有效的 accuracy 数据")
            continue

        labels.append(label)
        results[label] = acc_map
        defaults[label] = get_default_accuracy("log", label)

    # 3. 两两比较
    pair_labels = []
    mean_diffs = []
    ci_dict = {cl: {"lowers": [], "uppers": []} for cl in conf_levels}
    default_diffs = []

    for a, b in itertools.combinations(labels, 2):
        # 对齐配置
        common_keys = set(results[a].keys()) & set(results[b].keys())
        if not common_keys:
            print(f"注意: {a} 和 {b} 没有共同的 config_id，跳过")
            continue
        diffs = [results[a][k] - results[b][k] for k in common_keys]

        # CI（bootstrap）
        mdiffs = {}
        lowers = {}
        uppers = {}
        for cl in conf_levels:
            mean, lo, up = ci_bootstrap(diffs, cl)
            mdiffs[cl] = mean
            lowers[cl] = lo
            uppers[cl] = up

        # 保存：用第一个置信度（如 95%）的 mean 作为主展示值
        pair_labels.append(f"{a}-{b}")
        mean_diffs.append(mdiffs[conf_levels[0]])
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
    plt.figure(figsize=(10, 6))

    colors = {0.95: "blue", 0.99: "orange"}

    # 误差条
    for cl, vals in ci_dict.items():
        lowers = np.array(vals["lowers"])
        uppers = np.array(vals["uppers"])
        yerr = np.array([mean_diffs - lowers, uppers - mean_diffs])
        plt.errorbar(
            x,
            mean_diffs,
            yerr=yerr,
            fmt='o',
            color=colors.get(cl, "gray"),
            label=f"{int(cl * 100)}% CI",
            capsize=5
        )

    # 均值点 
    plt.scatter(x, mean_diffs, color='green', s=40, label='Mean', zorder=5)

    # # 在均值点旁边标注数值
    # for i, m in enumerate(mean_diffs):
    #     plt.annotate(
    #         f"{m:.3f}",
    #         xy=(x[i], m),
    #         xytext=(3, 3),       # 向右上稍微偏移一点，避免挡住点
    #         textcoords="offset points",
    #         fontsize=4,
    #         color="green"
    #     )

    # 默认值差异 + 标注
    for i, d in enumerate(default_diffs):
        if d is not None:
            plt.scatter(
                x[i],
                d,
                color='purple',
                s=40,
                label='Default' if i == 0 else "",
                zorder=5
            )
            # plt.annotate(
            #     f"{d:.3f}",
            #     xy=(x[i], d),
            #     xytext=(3, -10),  # 向右下偏移，避免和均值标注重叠
            #     textcoords="offset points",
            #     fontsize=4,
            #     color="purple"
            # )

    plt.axhline(0, color='gray', linestyle='--')
    plt.xticks(x, prettify_labels(pair_labels), fontsize=8, rotation=30, ha='right')
    plt.ylabel("Accuracy Difference", fontsize=10)
    plt.legend()
    plt.tight_layout()
    plt.savefig("llm_accuracy_diff2.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="比较不同模型之间配置准确率的差异及置信区间（固定9个label，支持同一label多文件）")
    parser.add_argument('--input_folder',default="ames_result_origin",help="包含日志文件的文件夹")
    parser.add_argument('--max_samples',type=int,default=500,help="默认采样样本数（若 LABEL_MAX_SAMPLES 中未指定该label时使用）")
    args = parser.parse_args()

    conf_levels = [0.95, 0.99]
    pair_labels, mean_diffs, ci_dict, default_diffs = process_differences(args.input_folder, args.max_samples, conf_levels)
    plot_differences(pair_labels, mean_diffs, ci_dict, default_diffs)