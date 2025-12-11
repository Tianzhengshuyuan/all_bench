# get_anova_all_accuracy使用重新测试的数据
import re
import ast
import os
import json
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
pattern1_mean = re.compile(
    r"总题组数:\s*(\d+).*?第一轮正确答案数:\s*\d+.*?正确率:\s*[\d.]+%.*?第二轮正确答案数:\s*(\d+).*?正确率:\s*([\d.]+)%"
)
pattern2_mean = re.compile(
    r"总题数:\s*(\d+).*?正确数:\s*(\d+).*?正确率:\s*([\d.]+)%,\s*耗时:"
)


CHAR_PER_TOKEN = {
    "yy": 5.3,     # English
    "zw": 1.7,     # 中文
    "ry": 1.0,     # 日语
    "ey": 3.8,     # 俄语
    "fy": 4.3,     # 法语
    "alby": 2.6,   # 阿拉伯语
}
SHORT_RATIO = 0.2

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

# 使用收敛法
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

# 使用大数定理
# LABEL_MAX_SAMPLES = {
#     "gpt41": 170,
#     "gpt35": 88,
#     "mistralM": 229,
#     "mistralL": 253,
#     "qwen": 218,       # qwen-plus
#     "qwen25": 329,     # qwen2.5
#     "deepseekv3": 285, # deepseek3
#     "doubao": 421,
#     "kimiv1": 63         # kimiv1
# }

def get_accuracies(logfile, max_samples=100):
    accuracies = []
    pattern_cfg = re.compile(r"处理key:\s*(\d+),\s*配置:\s*(\{.*\})")

    with open(logfile, "r", encoding="utf-8") as f:
        all_lines = f.readlines()

    current_key = None
    current_cfg = None
    current_lines = []
    seen_cfgs = set()

    def process_block(cfg, lines, key):
        """内层函数，用于处理单个配置块并返回调整后准确率"""
        if not cfg or not lines:
            return None

        mul = cfg.get("mul", 0)
        cot = cfg.get("cot", 0)
        language = cfg.get("language", "yy")
        max_tokens = int(cfg.get("max_tokens", 0))
        char_per_token = CHAR_PER_TOKEN.get(language, 3.0)
        effective_threshold = max_tokens * char_per_token * SHORT_RATIO

        # 收集所有回答段（与 compute_accuracy_with_adjust 同逻辑）
        answers = []
        current_content = []
        inside = False

        if mul == 1:
            start_pattern = re.compile(r"回答:") 
            correct_pattern = re.compile(r"正确答案是:")
        else:
            start_pattern = re.compile(r"回答:")
            correct_pattern = re.compile(r"正确答案:")

        for line in lines:
            if start_pattern.search(line):
                if inside:
                    answers.append("\n".join(current_content).strip())
                    current_content = []
                inside = True
                after = line.split(":", 1)[-1]
                current_content = [after.strip()]
                continue

            if correct_pattern.search(line):
                if inside:
                    answers.append("\n".join(current_content).strip())
                    current_content = []
                    inside = False
                continue

            if inside:
                current_content.append(line.strip())

        if inside and current_content:
            answers.append("\n".join(current_content).strip())

        # === 检查无效回答 ===
        N = 0
        for idx, content in enumerate(answers, 1):
            if mul == 1:
                if idx % 2 == 0 and len(content) < effective_threshold and check_invalid(content):
                    # print(f"[INVALID] file={logfile}, key={key}, idx={int(idx/2)}, len={len(content)}, thr={effective_threshold:.1f}, max={max_tokens}, cot={cot}, lang={language}, content={content}, 内容无效")
                    N += 1
            else:
                if len(content) < effective_threshold and check_invalid(content):
                    # print(f"[INVALID] file={logfile}, key={key}, idx={idx}, len={len(content)}, thr={effective_threshold:.1f}, max={max_tokens}, cot={cot}, lang={language}, content={content}, 内容无效")
                    N += 1

        # === 匹配准确率 (pattern1_mean / pattern2_mean) ===
        joined = "".join(lines)
        m1 = pattern1_mean.search(joined)
        m2 = pattern2_mean.search(joined)
        if m1:
            total = int(m1.group(1))
            correct = int(m1.group(2))
            acc_raw = float(m1.group(3)) / 100.0
            acc_adj = correct / (total) if total > N and total > 0 else acc_raw
            # acc_adj = correct / (total - N) if total > N and total > 0 else acc_raw
            # if N > 0:
            #     print(f"[ADJUST] key={key}, 原始acc={acc_raw:.4f}, 修正后={acc_adj:.4f}")
            return acc_adj
        elif m2:
            total = int(m2.group(1))
            correct = int(m2.group(2))
            acc_raw = float(m2.group(3)) / 100.0
            acc_adj = correct / (total) if total > N and total > 0 else acc_raw
            # acc_adj = correct / (total - N) if total > N and total > 0 else acc_raw
            # if N > 0:
            #     print(f"[ADJUST] key={key}, 原始acc={acc_raw:.4f}, 修正后={acc_adj:.4f}")          
            return acc_adj
        return None

    # === 遍历文件行按配置块划分 ===
    for line in all_lines:
        m_cfg = pattern_cfg.search(line)
        if m_cfg:
            # 遇到新配置前，先处理旧块
            if current_cfg is not None and current_lines:
                cfg_key = frozenset(current_cfg.items())
                if cfg_key not in seen_cfgs:
                    acc = process_block(current_cfg, current_lines, current_key)
                    if acc is not None:
                        accuracies.append(acc)
                        seen_cfgs.add(cfg_key)
                current_lines = []

            # 提取新的配置
            current_key = int(m_cfg.group(1))
            try:
                current_cfg = ast.literal_eval(m_cfg.group(2))
            except Exception as e:
                print(f"[WARN] 配置解析失败: {e} → {line.strip()}")
                current_cfg = None
            continue

        if current_cfg is not None:
            current_lines.append(line)

        if len(accuracies) >= max_samples:
            break

    # 处理最后一个配置块
    if current_cfg is not None and current_lines:
        cfg_key = frozenset(current_cfg.items())
        if cfg_key not in seen_cfgs:
            acc = process_block(current_cfg, current_lines, current_key)
            if acc is not None:
                accuracies.append(acc)
                seen_cfgs.add(cfg_key)
    return np.array(accuracies[:max_samples])

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

def check_invalid(content):
    pattern_mark = re.compile(r"####[^#\n]*####")
    pattern_mark2 = re.compile(r"####[^=\n]*###")
    pattern_mark3 = re.compile(r"###[^=\n]*####")
    # ####A  ~  ####D，末尾没有####
    pattern_single_letter = re.compile(r"####[A-D](?!#)")

    has_boxed = "\boxed" in content
    has_marked = bool(pattern_mark.search(content))
    has_marked2 = bool(pattern_mark2.search(content))
    has_marked3 = bool(pattern_mark3.search(content))
    has_single_letter = bool(pattern_single_letter.search(content))

    # 若没有 boxed，也没有任何命中标记，判定为无效
    if not (has_boxed or has_marked or has_marked2 or has_marked3 or has_single_letter):
        return True
    return False

def compute_accuracy_with_adjust(block_lines, cfg, key, label, logfile):
    mul = cfg.get("mul", 0)
    max_tokens = int(cfg.get("max_tokens", 0))
    cot = cfg.get("cot", 0)
    language = cfg.get("language", "yy")  # 默认英语

    char_per_token = CHAR_PER_TOKEN.get(language, 3.0)
    effective_char_threshold = max_tokens * char_per_token * SHORT_RATIO

    # === 合并答案段 ===
    answers = []  # [(label, content)]
    current_label, current_content = None, []

    if mul == 1:
        # 精确匹配传入的 label，例如 deepseek回答:
        start_pattern = re.compile(fr"{re.escape(label)}回答:")
        correct_pattern = re.compile(r"正确答案是:")
    else:
        start_pattern = re.compile(r"回答:")
        correct_pattern = re.compile(r"正确答案:")

    for line in block_lines:
        # 如果检测到新的“xxx回答:”行
        m_start = start_pattern.search(line)
        if m_start:
            # 若前面有未封闭回答，则保存
            if current_label is not None:
                merged_content = "\n".join(current_content).strip()
                answers.append((current_label, merged_content))
            # 开启新回答段
            current_label = label
            after_colon = line.split(":", 1)[-1] if ":" in line else ""
            current_content = [after_colon.strip()]
            continue

        # 碰到结尾标志（正确答案行）
        if correct_pattern.search(line):
            if current_label is not None:
                merged_content = "\n".join(current_content).strip()
                answers.append((current_label, merged_content))
                current_label, current_content = None, []
            continue

        # 如果当前在回答段中，累加该行内容
        if current_label is not None:
            current_content.append(line.rstrip("\n"))

    # 文件末尾还在回答中
    if current_label is not None:
        merged_content = "\n".join(current_content).strip()
        answers.append((current_label, merged_content))

    suppl_path = os.path.join("supplementary_logs", f"supplementary_log_{label}.txt")

    if os.path.exists(suppl_path):
        try:
            with open(suppl_path, "r", encoding="utf-8") as f:
                records = []
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        records.append(data)
                    except json.JSONDecodeError:
                        print(f"Warning: invalid JSON line in {suppl_path}: {line[:100]}...")
        except Exception as e:
            print(f"Error reading supplementary log {suppl_path}: {e}")
            records = []
    else:
        print(f"[INFO] supplementary log not found for label={label}: {suppl_path}")
        records = []
        
    # === 统计回答过短的情况 ===
    N = 0
    last_odd = -1
    if mul == 1:
        for idx, (_, content) in enumerate(answers, start=1):
            if len(content) < effective_char_threshold and check_invalid(content):
                if idx % 2 == 1:
                    last_odd = idx
                else:
                    if last_odd == idx - 1:
                        continue
                print(f"file={logfile}, key={key}, idx={int((idx+1)/2)}, max={max_tokens}, cot={cot}, lang={language}, len of content is {len(content)}, threshold is {effective_char_threshold}, content is {content}, invalid detected.")
                for record in records:
                    rec_file = record.get("file")
                    rec_idx = record.get("idx")
                    rec_cfg = record.get("cfg")
                    rec_new_right = record.get("new_right")
                    # print("record:", record)
                    # 严格匹配条件
                    if rec_file == logfile and rec_idx == int((idx+1)/2) and rec_cfg == cfg: 
                        print("cfg matched.")
                        if rec_new_right == 1:
                            N += 1
                            print(f"Matched supplementary_log: file2={rec_file}, key={key}, idx={int((idx+1)/2)}, new_right={rec_new_right}, N+1")
                            break  # 一个匹配即可，无需重复统计
    else:
        for idx, (_, content) in enumerate(answers, start=1):
            if len(content) < effective_char_threshold and check_invalid(content):
                print(f"file={logfile}, key={key}, idx={idx}, max={max_tokens}, cot={cot}, lang={language}, len of content is {len(content)}, threshold is {effective_char_threshold}, content is {content}, invalid detected.")
                for record in records:
                    rec_file = record.get("file")
                    rec_idx = record.get("idx")
                    rec_cfg = record.get("cfg")
                    rec_new_right = record.get("new_right")

                    # 严格匹配条件
                    if rec_file == logfile and rec_idx == idx and isinstance(rec_cfg, dict) and rec_cfg == cfg: 
                        print("cfg matched.")
                        if rec_new_right == 1:
                            N += 1
                            print(f"Matched supplementary_log: file2={rec_file}, key={key}, idx={idx}, new_right={rec_new_right}, N+1")
                            break  # 一个匹配即可，无需重复统计

    # === 匹配准确率 ===
    joined = "".join(block_lines)
    m1 = pattern1_mean.search(joined)
    m2 = pattern2_mean.search(joined)

    adjusted_acc = None
    if m1:
        total = int(m1.group(1))
        correct = int(m1.group(2))
        acc = float(m1.group(3)) / 100.0
        adjusted_acc = (correct + N) / total if total > (N + correct) else acc
        if N != 0:
            print(f"[key={key}] 配置调整: language={language}, N={N}, 原始准确率={acc:.4f}, 修正后准确率={adjusted_acc:.4f}")
    elif m2:
        total = int(m2.group(1))
        correct = int(m2.group(2))
        acc = float(m2.group(3)) / 100.0
        adjusted_acc = (correct + N) / total if total > (N + correct) else acc
        if N != 0:
            print(f"[key={key}] 配置调整: language={language}, N={N}, 原始准确率={acc:.4f}, 修正后准确率={adjusted_acc:.4f}")
    return adjusted_acc

def get_anova_all_accuracy(label, consider_vars=None):
    """
    从 anova_all 和 anova_all2 文件夹中读取与 label 匹配的日志，提取配置+准确率，
    在匹配 consider_vars 的基础上，利用 compute_accuracy_with_adjust() 对回答过短的样本
    进行剔除或修正，然后计算平均准确率。
    """
    folders = ["anova_all", "anova_all2"]
    existing_folders = [f for f in folders if os.path.exists(f)]
    if not existing_folders:
        print(f"[WARN] 没有找到 anova_all 或 anova_all2 文件夹。")
        return None

    if consider_vars is None:
        consider_vars = []
        print(f"{label} 未指定 consider_vars，返回 None")
        return None

    # ====== 生成配置搜索空间 ======
    target_configs = generate_config_space(consider_vars)
    print(f"{label} 生成 {len(target_configs)} 个目标配置组合")

    # 匹配 “key=xx, 配置={...}” 的正则
    key_cfg_pattern = re.compile(r"key\s*=\s*(\d+),\s*配置=(\{.*\})")

    results = []
    seen_cfgs = set()

    for folder in existing_folders:
        for fname in os.listdir(folder):
            if f"_{label}_" not in fname:
                continue
            filepath = os.path.join(folder, fname)
            print(f"[INFO] 读取 {filepath}")

            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()

            current_key = None
            current_cfg = None
            current_lines = []

            for line in lines:
                # === 匹配配置起始行，如：
                # 2025-09-09 09:00:51,450 - INFO - 开始处理配置 key=0, 配置={'language': 'fy', 'cot': 0, ...}
                m_key_cfg = key_cfg_pattern.search(line)
                if m_key_cfg:
                    # 如果前一个配置块未空，则先收尾处理
                    if current_cfg is not None and current_lines:
                        for target_cfg in target_configs:
                            if config_match(current_cfg, target_cfg):
                                cfg_key = frozenset(current_cfg.items())
                                if cfg_key not in seen_cfgs:
                                    acc_adj = compute_accuracy_with_adjust(
                                        current_lines,
                                        current_cfg,
                                        key=current_key,
                                        label=label,
                                        logfile=filepath
                                    )
                                    if acc_adj is not None:
                                        results.append(acc_adj)
                                        seen_cfgs.add(cfg_key)
                                break
                        current_lines = []

                    # 启动新配置块
                    current_key = int(m_key_cfg.group(1))
                    try:
                        current_cfg = ast.literal_eval(m_key_cfg.group(2))
                    except Exception as e:
                        print(f"[WARN] 无法解析配置行: {e} → {line.strip()}")
                        current_cfg = None
                    continue

                # 累加当前块内容
                if current_cfg is not None:
                    current_lines.append(line)

            # === 处理最后一个配置块 ===
            if current_cfg is not None and current_lines:
                for target_cfg in target_configs:
                    if config_match(current_cfg, target_cfg):
                        cfg_key = frozenset(current_cfg.items())
                        if cfg_key not in seen_cfgs:
                            acc_adj = compute_accuracy_with_adjust(
                                current_lines,
                                current_cfg,
                                key=current_key,
                                label=label,
                                logfile=filepath
                            )
                            if acc_adj is not None:
                                results.append(acc_adj)
                                seen_cfgs.add(cfg_key)
                        break

    if not results:
        print(f"[INFO] {label} 没有匹配的配置数据。")
        return None

    mean_acc = float(np.mean(results))
    print(f"[INFO] Found {len(results)} unique adjusted accuracies for label {label}. 平均准确率={mean_acc:.4f}")
    return mean_acc

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
        if label == "gpt41" or label == "doubao" or label == "mistralL" or label == "qwen":
            continue
        # 使用对应 label 的 max_samples，否则用默认参数 max_samples
        label_max_samples = LABEL_MAX_SAMPLES.get(label, max_samples)
        accuracies = get_accuracies(log, label_max_samples)
        # accuracies = get_accuracies(log, max_samples)
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
            plt.text(x[i] + 0.1, acc + 0.002,f"{acc:.4f}", fontsize=9,color='black',ha='left',va='bottom')
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
    plt.savefig('llm_accuracy_ci_with_truth4.png', dpi=300)
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