import re
import ast
import os
import argparse
import itertools
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# 正则模式
pattern1 = re.compile(
    r"总题组数:\s*\d+.*?第一轮正确答案数:\s*\d+.*?正确率:\s*[\d.]+%.*?第二轮正确答案数:\s*\d+.*?正确率:\s*([\d.]+)%"
)
pattern2 = re.compile(
    r"总题数:\s*\d+.*?正确数:\s*\d+.*?正确率:\s*([\d.]+)%,\s*耗时:"
)


# ===== 全局变量定义 =====
VARIABLES = {
    "language": (["alby","ey","fy","ry","yy","zw"], "yy"),
    "cot": ([0,1], 0),
    "few": ([0,1], 0),
    "mul": ([0,1], 0),
    "Temperature": ([0.0,1.0,2.0], 1.0),
    "max_tokens": ([10,100,4000], 4000),
    "top_p": ([0.2,0.6,1.0], 0.6),
    "presence_penalty": ([-0.5,0.5,1.5], 0.5),
    "question_type": ([0,1], 0),
    "question_tran": ([0,1], 0),
}

LABEL_CONSIDER_VARS = {
    "deepseekv3": ["question_type", "cot", "max_tokens", "few", "language"],
    "doubao": ["question_type", "cot", "max_tokens", "presence_penalty", "few"],
    "kimiv1": ["question_type", "cot", "mul", "few", "language"],
    "qwen": ["question_type", "cot", "max_tokens", "few", "language"],
    "qwen25": ["question_type", "cot", "max_tokens", "few", "mul"],
    "gpt35": ["question_type", "cot", "mul", "few", "Temperature"],
    "gpt41": ["question_type", "cot", "max_tokens", "Temperature", "top_p"],
    "mistralL": ["question_type", "cot", "max_tokens", "mul", "few"],
    "mistralM": ["question_type", "cot", "max_tokens", "few", "mul"]
}


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

LABEL_MAX_SAMPLES = {
    "gpt41": 170,
    "gpt35": 88,
    "mistralM": 229,
    "mistralL": 253,
    "qwen": 218,       # qwen-plus
    "qwen25": 329,     # qwen2.5
    "deepseekv3": 285, # deepseek3
    "doubao": 421,
    "kimiv1": 63         # kimiv1
}

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
    return np.array(accuracies)


def generate_config_space(consider_vars):
    """根据考虑的变量生成配置组合"""
    keys = list(consider_vars)
    domains = []
    for k in keys:
        domains.append(VARIABLES[k][0])
    combos = list(itertools.product(*domains))
    config_list = []
    for combo in combos:
        config = {}
        # 考虑的变量
        for i, k in enumerate(keys):
            config[k] = combo[i]
        # 其他用默认值
        for k in VARIABLES:
            if k not in config:
                config[k] = VARIABLES[k][1]
        config_list.append(config)
    return config_list

def parse_config(line):
    """从配置行解析出dict"""
    m = re.search(r"配置=(\{.*\})", line)
    if m:
        config_str = m.group(1)
        try:
            config = ast.literal_eval(config_str)
            return config
        except Exception as e:
            print("解析配置失败:", e, line)
    return None

def config_match(cfg, target_cfg):
    """比较单个配置是否等于目标配置（所有字段都一样）"""
    for k,v in target_cfg.items():
        if k not in cfg or str(cfg[k]) != str(v):
            return False
    return True

def get_anova_all_accuracy(label, consider_vars=None):
    """
    从 anova_all 和 anova_all2 文件夹中读取与 label 匹配的日志，提取配置+准确率，
    仅保留匹配 consider_vars 所有组合的accuracy，去除重复配置后求平均。
    """
    folders = ["anova_all", "anova_all2"]
    existing_folders = [f for f in folders if os.path.exists(f)]
    if not existing_folders:
        return None
    
    if consider_vars is None:
        consider_vars = []
        print(f"{label} 未指定 consider_vars，返回 None")
    target_configs = generate_config_space(consider_vars)
    print(f"{label} 生成 {len(target_configs)} 个目标配置组合")

    results = []
    seen_cfgs = set()  # 存放已处理的配置，避免重复
    
    for folder in existing_folders:
        for fname in os.listdir(folder):
            if f"_{label}_" not in fname:
                continue
            filepath = os.path.join(folder, fname)
            with open(filepath, 'r', encoding='utf-8') as f:
                current_cfg = None
                for line in f:
                    # 先抓配置
                    if ", 配置={" in line:
                        cfg = parse_config(line)
                        if cfg:
                            current_cfg = cfg
                        continue
                    # 如果有当前配置，找下一个accuracy
                    if current_cfg is not None:
                        m1 = pattern1.search(line)
                        m2 = pattern2.search(line)
                        acc = None
                        if m1:
                            acc = float(m1.group(1)) / 100.0
                        elif m2:
                            acc = float(m2.group(1)) / 100.0
                        if acc is not None:
                            for target_cfg in target_configs:
                                if config_match(current_cfg, target_cfg):
                                    # 用 frozenset 作为 hashable key 去重
                                    cfg_key = frozenset(current_cfg.items())
                                    if cfg_key not in seen_cfgs:
                                        results.append(acc)
                                        seen_cfgs.add(cfg_key)
                                    break
                            current_cfg = None  # 一个配置只取一次accuracy
    
    if not results:
        print(f"{label} 没有匹配的配置数据")
        return None
    print(f"Found {len(results)} unique matching accuracies for label {label}")
    return float(np.mean(results))

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

    labels, means, anova_all_accs, default_accs = [], [], [], []
    ci_dict = {cl: {"lowers": [], "uppers": []} for cl in conf_levels}

    for log in sorted(log_files):
        label = extract_label_from_filename(log)
        # 使用对应 label 的 max_samples，否则用默认参数 max_samples
        label_max_samples = LABEL_MAX_SAMPLES.get(label, max_samples)
        # accuracies = get_accuracies(log, label_max_samples)
        accuracies = get_accuracies(log, max_samples)
        if len(accuracies) == 0:
            print(f"{log} 未提取到数据，跳过。")
            continue
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
                anova_all_acc = get_anova_all_accuracy(label, LABEL_CONSIDER_VARS.get(label, []))
                anova_all_accs.append(anova_all_acc)
                default_acc = get_default_accuracy(input_folder, label)
                default_accs.append(default_acc)
            ci_dict[cl]["lowers"].append(ci_lower)
            ci_dict[cl]["uppers"].append(ci_upper)

    return labels, np.array(means), ci_dict, anova_all_accs, default_accs

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

def plot_results(labels, means, ci_dict, anova_all_accs, default_accs):
    x = np.arange(len(labels))
    plt.figure(figsize=(6,6))

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
    plt.scatter(x, means, color='green', s=30, zorder=5, label='Mean')
    print(labels, means)

    # ground truth准确率红叉
    for i, acc in enumerate(anova_all_accs):
        if acc is not None:
            plt.scatter(x[i], acc, color='red', marker='D', s=50, label='Ground Truth (restricted space)' if i == 0 else "")
            print(f"Ground Truth for {labels[i]}: {acc:.4f}")

    # 默认准确率
    for i, acc in enumerate(default_accs):
        if acc is not None:
            plt.scatter(x[i], acc, color='purple', s=50, label='Default' if i == 0 else "")
            
    plt.xticks(x, prettify_labels(labels), fontsize=10, rotation=20, ha='right')
    plt.ylabel('Accuracy', fontsize=14)
    plt.xlabel('LLM', fontsize=14)
    # plt.title('Accuracy and Confidence Intervals for LLMs', fontsize=15, weight='bold')
    plt.ylim(0, 0.5)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig('llm_accuracy_ci_with_truth2.png', dpi=300)
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
    labels, means, ci_dict, anova_all_accs, default_accs = process_logs(args.input_folder, args.N, args.max_samples, args.method, conf_levels)
    plot_results(labels, means, ci_dict, anova_all_accs, default_accs)