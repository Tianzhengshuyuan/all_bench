import os
import re
import numpy as np
import matplotlib.pyplot as plt

# === 正则匹配规则 ===
pattern1 = re.compile(
    r"总题组数:\s*(\d+).*?第一轮正确答案数:\s*\d+.*?正确率:\s*[\d.]+%.*?第二轮正确答案数:\s*(\d+).*?正确率:\s*([\d.]+)%"
)
pattern2 = re.compile(
    r"总题数:\s*(\d+).*?正确数:\s*(\d+).*?正确率:\s*([\d.]+)%,\s*耗时:"
)

pattern1_dtb = re.compile(
    r"总题组数:\s*\d+.*?第一轮正确答案数:\s*\d+.*?正确率:\s*[\d.]+%.*?第二轮正确答案数:\s*\d+.*?正确率:\s*([\d.]+)%"
)
pattern2_dtb = re.compile(
    r"总题数:\s*\d+.*?正确数:\s*\d+.*?正确率:\s*([\d.]+)%,\s*耗时:"
)

# 匹配配置：default vs log
config_pattern_default = re.compile(
    r"开始处理配置 key=(\d+),\s*配置=({.*?})"
)
config_pattern_log = re.compile(
    r"处理key:\s*(\d+),\s*配置:\s*({.*?})"
)
config_pattern_default_dtb = re.compile(r"配置 key=(\d+),\s*配置=.*")
config_pattern_log_dtb = re.compile(r"处理key:\s*(\d+),\s*配置:\s*\{.*?\}")


# 匹配回答与正确答案
answer_pattern = re.compile(r"(\w+)回答:\s*(.*?)\s*正确答案是:")
# === 基准 accuracy ===
BASE_ACCURACIES = {
    "deepseekv3": 39.2 / 100.0,
    "gpt41": 48.1 / 100.0,
    "kimik2": 69.6 / 100.0,
    "qwen3": 32.8 / 100.0,
}

FOLDERS = [
    # "log",
    "ames_result_origin",
    "ames_result_disturb1",
    "ames_result_disturb2",
    "ames_result_disturb3",
    "ames_result_analogical",
    "ames_result_compose"
]

FOLDER_LABELS = {
    # "log": "origin",
    "ames_result_origin": "origin",
    "ames_result_disturb1": "disturb1",
    "ames_result_disturb2": "disturb2",
    "ames_result_disturb3": "disturb3",
    "ames_result_analogical": "analogical",
    "ames_result_compose": "compose",
}

# === 语言映射：字符数/每个token的平均量 ===
CHAR_PER_TOKEN = {
    "yy": 5.3,     # English
    "zw": 1.7,     # 中文
    "ry": 1.0,     # 日语
    "ey": 3.8,     # 俄语
    "fy": 4.3,     # 法语
    "alby": 2.6,   # 阿拉伯语
}
SHORT_RATIO = 0.3

def safe_eval_dict(raw_text):
    """安全地将配置字符串解析为字典。"""
    try:
        return eval(raw_text.strip())
    except Exception:
        return {}

def check_invalid(content):
    pattern_mark = re.compile(r"####[^#\n]*####")
    has_boxed = "\\boxed" in content
    has_marked = bool(pattern_mark.search(content))
    if not has_boxed and not has_marked:
        return True
    return False

def prettify_labels(labels):
    mapping = {
        "deepseekv3": "deepseek-v3",
        "doubao": "doubao-1.5-pro",
        "kimiv1": "moonshot-v1-8k",
        "qwen25": "qwen2.5-32b",
    }
    return [mapping.get(lbl, lbl) for lbl in labels]

def compute_accuracy_with_adjust(block_lines, cfg, key, label, logfile):
    """
    解析一个配置块日志，支持多行回答文本。
    根据 mul, max_tokens, language 等计算修正准确率。
    """

    mul = cfg.get("mul", 0)
    max_tokens = int(cfg.get("max_tokens", 0))
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

    # === 统计回答过短的情况 ===
    N = 0
    if mul == 1:
        for idx, (_, content) in enumerate(answers, start=1):
            # print(f"content is {content}")
            if idx % 2 == 0 and len(content) < effective_char_threshold and check_invalid(content):
                # print(f"file={logfile}, key={key}, idx={idx}, max={max_tokens}, lang={language} len of content is {len(content)}, threshold is {effective_char_threshold}, invalid detected.")
                N += 1
    else:
        for idx, (_, content) in enumerate(answers, start=1):
            # print(f"content is {content}")
            if len(content) < effective_char_threshold and check_invalid(content):
                # print(f"file={logfile}, key={key}, idx={idx}, max={max_tokens}, lang={language} len of content is {len(content)}, threshold is {effective_char_threshold}, invalid detected.")
                N += 1

    # === 匹配准确率 ===
    joined = "".join(block_lines)
    m1 = pattern1.search(joined)
    m2 = pattern2.search(joined)

    adjusted_acc = None
    if m1:
        total = int(m1.group(1))
        correct = int(m1.group(2))
        acc = float(m1.group(3)) / 100.0
        adjusted_acc = correct / (total - N) if total > N and total > 0 else acc
        if N != 0:
            print(f"[key={key}] 配置调整: language={language}, N={N}, 原始准确率={acc:.4f}, 修正后准确率={adjusted_acc:.4f}")
    elif m2:
        total = int(m2.group(1))
        correct = int(m2.group(2))
        acc = float(m2.group(3)) / 100.0
        adjusted_acc = correct / (total - N) if total > N and total > 0 else acc
        if N != 0:
            print(f"[key={key}] 配置调整: language={language}, N={N}, 原始准确率={acc:.4f}, 修正后准确率={adjusted_acc:.4f}")
    return adjusted_acc

def get_key_accuracies_for_mean(logfile, folder_name, label):
    """解析日志文件：提取key、配置参数、修正accuracy。"""
    if folder_name == "log":
        config_pattern = config_pattern_log
    else:
        config_pattern = config_pattern_default

    key_acc_map = {}
    current_key = None
    current_cfg = None
    current_lines = []
    print(f"[INFO] 解析日志文件: {logfile}, 文件夹: {folder_name}")
    with open(logfile, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        # ---- 匹配配置 ----
        m_cfg = config_pattern.search(line)
        if m_cfg:
            # 如果之前有一个未处理的配置，先处理完它
            if current_key is not None and current_cfg is not None and current_lines:
                acc_val = compute_accuracy_with_adjust(current_lines, current_cfg, current_key, label, logfile)
                if acc_val is not None:
                    key_acc_map[current_key] = acc_val

            # 启动新配置
            current_key = int(m_cfg.group(1))
            current_cfg = safe_eval_dict(m_cfg.group(2))
            current_lines = []
            continue

        # 如果正在记录一段配置块内的内容
        if current_key is not None:
            current_lines.append(line)

    # 文件结束后处理最后一个配置块
    if current_key is not None and current_cfg is not None and current_lines:
        acc_val = compute_accuracy_with_adjust(current_lines, current_cfg, current_key, label, logfile)
        if acc_val is not None:
            key_acc_map[current_key] = acc_val

    return key_acc_map

def get_key_accuracies_for_distribution(logfile, folder_name):
    """解析日志文件：提取配置key和对应accuracy。"""
    if folder_name == "log":
        config_pattern = config_pattern_log_dtb
    else:
        config_pattern = config_pattern_default_dtb

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
            m1 = pattern1_dtb.search(line)
            m2 = pattern2_dtb.search(line)
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

def get_violin(max_samples=500, diff=False, output="violin_multi_folder.png"):
    target_labels = ["deepseekv3", "doubao", "kimiv1", "qwen25"]
    all_data_mean = {folder: {lbl: {} for lbl in target_labels} for folder in FOLDERS}
    all_data_dist = {folder: {lbl: {} for lbl in target_labels} for folder in FOLDERS}

    # === 读取并整合数据 ===
    for folder in FOLDERS:
        if not os.path.exists(folder):
            print(f"[WARN] 文件夹 {folder} 不存在，跳过。")
            continue

        all_files = [f for f in os.listdir(folder) if f.startswith("sample_test_") and f.endswith(".log")]
        if not all_files:
            print(f"[WARN] 文件夹 {folder} 中未找到日志文件。")
            continue

        for f in all_files:
            for lbl in target_labels:
                if lbl in f:
                    path = os.path.join(folder, f)
                    try:
                        # 分别计算均值基准与分布数据
                        key_acc_map_for_mean = get_key_accuracies_for_mean(path, folder, lbl)
                        key_acc_map_for_distribution = get_key_accuracies_for_distribution(path, folder)

                        # 存储到对应的结构中
                        if key_acc_map_for_mean:
                            for k, v in key_acc_map_for_mean.items():
                                all_data_mean[folder][lbl][k] = v

                        if key_acc_map_for_distribution:
                            for k, v in key_acc_map_for_distribution.items():
                                all_data_dist[folder][lbl][k] = v

                    except Exception as e:
                        print(f"[ERROR] 文件 {path} 解析失败: {e}")

    # === 缺失key检查 ===
    print("\n=== 缺失配置检查报告 ===")
    for folder in FOLDERS:
        if folder not in all_data_mean:
            continue
        for lbl in target_labels:
            keys = sorted(k for k in all_data_mean[folder][lbl].keys() if 0 <= k < max_samples)
            expected = set(range(max_samples))
            existing = set(keys)
            missing = sorted(expected - existing)
            if missing:
                print(
                    f"[MISSING] {folder} -> {lbl}: 缺少 {len(missing)} 个配置 "
                    f"(例如 key={missing[:15]}{'...' if len(missing) > 15 else ''})"
                )
            else:
                print(f"[OK] {folder} -> {lbl}: 0–{max_samples-1} 全部配置齐全。")

    # === 绘图 ===
    plt.figure(figsize=(14, 7))
    colors = ["#9975a6", "#519aba", "#ea6864", "#ffb347", "#7dcfb6", "#a0c4ff"]
    positions, data_to_plot, mean_vals, median_vals = [], [], [], []

    for i, lbl in enumerate(target_labels):
        base_pos = i * (len(FOLDERS) + 1)
        for j, folder in enumerate(FOLDERS):
            label_data_dist = all_data_dist[folder][lbl]
            label_data_mean = all_data_mean[folder][lbl]

            accs_dist = np.array(
                [label_data_dist[k] for k in sorted(label_data_dist.keys()) if 0 <= k < max_samples]
            )
            accs_mean = np.array(
                [label_data_mean[k] for k in sorted(label_data_mean.keys()) if 0 <= k < max_samples]
            )

            if len(accs_dist) == 0 or len(accs_mean) == 0:
                continue

            if diff and lbl in BASE_ACCURACIES:
                accs_dist = accs_dist - BASE_ACCURACIES[lbl]
                accs_mean = accs_mean - BASE_ACCURACIES[lbl]

            positions.append(base_pos + j)
            data_to_plot.append(accs_dist)
            mean_vals.append(np.mean(accs_mean))
            median_vals.append(np.median(accs_mean))

    if not data_to_plot:
        print("[ERROR] 没有可绘制的数据。")
        return

    parts = plt.violinplot(
        data_to_plot,
        positions=positions,
        widths=0.6,
        showmeans=False,
        showmedians=False,
        showextrema=True,
    )
    
    # === 绘制手动 Mean / Median ===
    for idx, pos in enumerate(positions):
        mean_val = mean_vals[idx]
        median_val = median_vals[idx]

        # 绿色均值线
        plt.hlines(y=mean_val, xmin=pos - 0.25, xmax=pos + 0.25,
                colors="green", linewidth=1, linestyles="-")

        # 红色中位数线
        plt.hlines(y=median_val, xmin=pos - 0.25, xmax=pos + 0.25,
                colors="red", linewidth=1, linestyles="--")

        # 标注文字
        plt.text(
            pos + 0.15, mean_val + 0.002, f"{mean_val*100:.2f}%", color="green",
            fontsize=8, ha="left", va="bottom", rotation=30
        )
        plt.text(
            pos + 0.15, median_val - 0.002, f"{median_val*100:.2f}%", color="red",
            fontsize=8, ha="left", va="top", rotation=30
        )
        
    # 调整 violin 样式
    for i, pc in enumerate(parts["bodies"]):
        pc.set_facecolor(colors[i % len(FOLDERS)])
        pc.set_alpha(0.7)

    # parts["cmeans"].set_color("green")
    # parts["cmedians"].set_color("red")
    parts["cmaxes"].set_color("#555")
    parts["cmins"].set_color("#555")
    parts["cbars"].set_color("#555")

    label_positions = [
        (i * (len(FOLDERS) + 1) + (len(FOLDERS) - 1) / 2)
        for i in range(len(target_labels))
    ]

    plt.xticks(label_positions, prettify_labels(target_labels), fontsize=14, rotation=30)
    plt.ylabel("Deviation from Reported Accuracy" if diff else "Accuracy", fontsize=16)
    plt.xlabel("LLM", fontsize=18)
    plt.yticks(fontsize=14)
    plt.grid(axis="y", linestyle="--", alpha=0.6)


    # === 图例 ===
    legend_handles = [
        plt.Line2D([0], [0], color=colors[i], lw=8, label=FOLDER_LABELS[FOLDERS[i]])
        for i in range(len(FOLDERS))
    ]
    legend_handles += [
        plt.Line2D([0], [0], color="green", lw=2, label="Mean"),
        plt.Line2D([0], [0], color="red", lw=2, label="Median"),
    ]

    plt.legend(
        handles=legend_handles,
        fontsize=11,
        loc="lower center",
        bbox_to_anchor=(0.5, 1.02),
        ncol=len(FOLDER_LABELS) + 2,
        frameon=False,
    )

    plt.tight_layout(rect=[0, 0, 1, 0.93])
    plt.savefig(output, dpi=300)
    plt.show()

    print(f"\n[DONE] 小提琴图已保存到 {output}")


if __name__ == "__main__":
    get_violin(max_samples=500, diff=False, output="violin_multi_folder_clean.png")