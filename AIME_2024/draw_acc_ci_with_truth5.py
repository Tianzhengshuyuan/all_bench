import re
import ast
import os
import argparse
import itertools
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# ===== 正则模式 =====
pattern1 = re.compile(
    r"总题组数:\s*\d+.*?第一轮正确答案数:\s*\d+.*?正确率:\s*[\d.]+%.*?第二轮正确答案数:\s*\d+.*?正确率:\s*([\d.]+)%"
)
pattern2 = re.compile(
    r"总题数:\s*\d+.*?正确数:\s*\d+.*?正确率:\s*([\d.]+)%,\s*耗时:"
)

# 匹配配置 key 的正则
config_pattern_default = re.compile(r"配置 key=(\d+),\s*配置=.*")


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
    "gpt41": 170,
    "gpt35": 88,
    "mistralM": 229,
    "mistralL": 253,
    "qwen": 218,
    "qwen25": 329,
    "deepseekv3": 285,
    "doubao": 421,
    "kimiv1": 63
}

# ===== 新的 get_key_accuracies 函数 =====
def get_key_accuracies(logfile, folder_name):

    config_pattern = config_pattern_default

    key_acc_map = {}
    current_key = None

    with open(logfile, "r", encoding="utf-8") as f:
        for line in f:
            # 匹配配置行
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

            if acc is not None and current_key is not None:
                if current_key not in key_acc_map:
                    key_acc_map[current_key] = acc
                current_key = None

    return key_acc_map


# ===== 其他函数保持不变 =====
def generate_config_space(consider_vars):
    keys = list(consider_vars)
    domains = []
    for k in keys:
        domains.append(VARIABLES[k][0])
    combos = list(itertools.product(*domains))
    config_list = []
    for combo in combos:
        config = {}
        for i, k in enumerate(keys):
            config[k] = combo[i]
        for k in VARIABLES:
            if k not in config:
                config[k] = VARIABLES[k][1]
        config_list.append(config)
    return config_list

def parse_config(line):
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
    for k,v in target_cfg.items():
        if k not in cfg or str(cfg[k]) != str(v):
            return False
    return True

def get_anova_all_accuracy(label, consider_vars=None):
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
    seen_cfgs = set()
    for folder in existing_folders:
        for fname in os.listdir(folder):
            if f"_{label}_" not in fname:
                continue
            filepath = os.path.join(folder, fname)
            with open(filepath, 'r', encoding='utf-8') as f:
                current_cfg = None
                for line in f:
                    if ", 配置={" in line:
                        cfg = parse_config(line)
                        if cfg:
                            current_cfg = cfg
                        continue
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
                                    cfg_key = frozenset(current_cfg.items())
                                    if cfg_key not in seen_cfgs:
                                        results.append(acc)
                                        seen_cfgs.add(cfg_key)
                                    break
                            current_cfg = None
    if not results:
        print(f"{label} 没有匹配的配置数据")
        return None
    print(f"Found {len(results)} unique matching accuracies for label {label}")
    return float(np.mean(results))

def ci_normal(accuracies, N, conf_level):
    n = len(accuracies)
    mean = np.mean(accuracies)
    std = np.std(accuracies, ddof=1)
    se = std / np.sqrt(n)
    fpc = np.sqrt((N - n) / (N - 1))
    se_fpc = se * fpc
    t_value = stats.t.ppf(1 - (1 - conf_level)/2, df=n-1)
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
    lower_percentile = 100*(alpha/2)
    upper_percentile = 100*(1-alpha/2)
    ci_lower = np.percentile(means, lower_percentile)
    ci_upper = np.percentile(means, upper_percentile)
    mean = np.mean(accuracies)
    return mean, ci_lower, ci_upper

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
    }
    return [mapping.get(lbl, lbl) for lbl in labels]

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

# ===== 主处理逻辑修改 =====
def process_logs(input_folder, N, method="normal", conf_levels=[0.95, 0.99]):
    """从 ames_result_origin 中提取每个固定 label 的 accuracies"""
    labels = ["deepseekv3", "doubao", "gpt35", "gpt41", "kimiv1", "mistralL", "mistralM", "qwen", "qwen25"]

    means, anova_all_accs, default_accs = [], [], []
    ci_dict = {cl: {"lowers": [], "uppers": []} for cl in conf_levels}

    for label in labels:
        print(f"==== 处理 {label} ====")
        all_acc_map = {}

        # 搜索文件夹中符合该 label 的文件
        for fname in os.listdir(input_folder):
            if f"_{label}_" not in fname:
                continue
            filepath = os.path.join(input_folder, fname)
            file_acc_map = get_key_accuracies(filepath, "log")
            for k, v in file_acc_map.items():
                # 收集 key: accuracy
                if k not in all_acc_map:
                    all_acc_map[k] = v

        label_max = LABEL_MAX_SAMPLES.get(label, 100)
        # 按 key 顺序取有效区间
        valid_accs = [all_acc_map[k] for k in sorted(all_acc_map.keys()) if k < label_max]
        valid_accs = np.array(valid_accs)
        if len(valid_accs) == 0:
            print(f"{label}: 无可用accuracy数据")
            continue

        # 计算置信区间
        for cl in conf_levels:
            if method == "normal":
                mean, ci_lower, ci_upper = ci_normal(valid_accs, N, cl)
            else:
                mean, ci_lower, ci_upper = ci_bootstrap(valid_accs, N, cl)
            if cl == conf_levels[0]:
                means.append(mean)
                anova_all_acc = get_anova_all_accuracy(label, LABEL_CONSIDER_VARS.get(label, []))
                anova_all_accs.append(anova_all_acc)
                default_acc = get_default_accuracy("log", label)
                default_accs.append(default_acc)
            ci_dict[cl]["lowers"].append(ci_lower)
            ci_dict[cl]["uppers"].append(ci_upper)

    return labels, np.array(means), ci_dict, anova_all_accs, default_accs


def plot_results(labels, means, ci_dict, anova_all_accs, default_accs):
    x = np.arange(len(labels))
    plt.figure(figsize=(6,6))
    colors = {0.95: "blue", 0.99: "orange"}

    for cl, vals in ci_dict.items():
        lowers = np.array(vals["lowers"])
        uppers = np.array(vals["uppers"])
        yerr = np.array([means - lowers, uppers - means])
        plt.errorbar(x, means, yerr=yerr, fmt='none', color=colors.get(cl,"gray"),
                     label=f'{int(cl*100)}% CI', capsize=6, elinewidth=2)

    plt.scatter(x, means, color='green', s=30, zorder=5, label='Mean')
    # 默认准确率
    for i, acc in enumerate(default_accs):
        if acc is not None:
            plt.scatter(x[i], acc, color='purple', s=50, label='Default' if i == 0 else "")
    for i, acc in enumerate(anova_all_accs):
        if acc is not None:
            plt.scatter(x[i], acc, color='red', marker='D', s=50, label='Ground Truth' if i==0 else "")

    plt.xticks(x, prettify_labels(labels), rotation=20, ha='right')
    plt.ylabel('Accuracy', fontsize=14)
    plt.xlabel('LLM', fontsize=14)
    plt.ylim(0,0.5)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig('llm_accuracy_ci_with_truth5.png', dpi=300)
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="根据配置key计算每个label的置信区间")
    parser.add_argument('--input_folder', default="ames_result_origin", help="日志文件夹")
    parser.add_argument('--N', type=int, default=15552, help="配置空间大小")
    parser.add_argument('--method', default="normal", choices=["normal","bootstrap"], help="计算方法")
    args = parser.parse_args()

    conf_levels = [0.95, 0.99]
    labels, means, ci_dict, anova_all_accs, default_accs = process_logs(args.input_folder, args.N, args.method, conf_levels)
    plot_results(labels, means, ci_dict, anova_all_accs, default_accs)