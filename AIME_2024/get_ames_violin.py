import os
import re
import numpy as np
import matplotlib.pyplot as plt

# === 正则匹配规则 ===
pattern1 = re.compile(
    r"总题组数:\s*\d+.*?第一轮正确答案数:\s*\d+.*?正确率:\s*[\d.]+%.*?第二轮正确答案数:\s*\d+.*?正确率:\s*([\d.]+)%"
)
pattern2 = re.compile(
    r"总题数:\s*\d+.*?正确数:\s*\d+.*?正确率:\s*([\d.]+)%,\s*耗时:"
)

# 两种配置格式
config_pattern_default = re.compile(r"配置 key=(\d+),\s*配置=.*")
config_pattern_log = re.compile(r"处理key:\s*(\d+),\s*配置:\s*\{.*?\}")

# === 基准 accuracy ===
BASE_ACCURACIES = {
    "deepseekv3": 39.2 / 100.0,
    "gpt41": 48.1 / 100.0,
    "kimik2": 69.6 / 100.0,
    "qwen3": 32.8 / 100.0,
}

# === 文件夹集合 ===
FOLDERS = [
    "log",
    "ames_result_disturb1",
    "ames_result_disturb2",
    "ames_result_disturb3",
    "ames_result_analogical",  # ✅ 新增 analogical 文件夹
]

FOLDER_LABELS = {
    "log": "origin",
    "ames_result_disturb1": "disturb1",
    "ames_result_disturb2": "disturb2",
    "ames_result_disturb3": "disturb3",
    "ames_result_analogical": "analogical",  # ✅ 新增标签
}


def get_key_accuracies(logfile, folder_name):
    """
    解析日志文件：提取配置key和对应accuracy。
    log/ 中使用 “处理key” 匹配；
    其他文件夹使用 “配置 key=” 匹配。
    """
    if folder_name == "log":
        config_pattern = config_pattern_log
    else:
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


def prettify_labels(labels):
    mapping = {
        "deepseekv3": "deepseek-v3",
        "doubao": "doubao-1.5-pro",
        "kimiv1": "moonshot-v1-8k",
        "qwen25": "qwen2.5-32b",
    }
    return [mapping.get(lbl, lbl) for lbl in labels]


def get_violin(max_samples=500, diff=False, output="violin_multi_folder.png"):
    target_labels = ["deepseekv3", "doubao", "kimiv1", "qwen25"]
    all_data = {folder: {lbl: {} for lbl in target_labels} for folder in FOLDERS}

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
                        key_acc_map = get_key_accuracies(path, folder)
                        if key_acc_map:
                            label_data = all_data[folder][lbl]
                            for k, v in key_acc_map.items():
                                if k not in label_data:
                                    label_data[k] = v
                    except Exception as e:
                        print(f"[ERROR] 文件 {path} 解析失败: {e}")

    # === 缺失key检查 ===
    print("\n=== 缺失配置检查报告 ===")
    for folder in FOLDERS:
        if folder not in all_data:
            continue
        for lbl in target_labels:
            keys = sorted(k for k in all_data[folder][lbl].keys() if 0 <= k < max_samples)
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
    plt.figure(figsize=(13, 7))
    colors = ["#9975a6", "#519aba", "#ea6864", "#ffb347", "#7dcfb6"]  # ✅ 增加1种颜色
    positions, data_to_plot, mean_vals, median_vals = [], [], [], []

    for i, lbl in enumerate(target_labels):
        base_pos = i * (len(FOLDERS) + 1)
        for j, folder in enumerate(FOLDERS):
            label_data = all_data[folder][lbl]
            accs = np.array(
                [label_data[k] for k in sorted(label_data.keys()) if 0 <= k < max_samples]
            )
            if len(accs) == 0:
                continue
            if diff and lbl in BASE_ACCURACIES:
                accs = accs - BASE_ACCURACIES[lbl]
            positions.append(base_pos + j)
            data_to_plot.append(accs)
            mean_vals.append(np.mean(accs))
            median_vals.append(np.median(accs))

    if not data_to_plot:
        print("[ERROR] 没有可绘制的数据。")
        return

    parts = plt.violinplot(
        data_to_plot,
        positions=positions,
        widths=0.6,
        showmeans=True,
        showmedians=True,
        showextrema=True,
    )

    for i, pc in enumerate(parts["bodies"]):
        pc.set_facecolor(colors[i % len(FOLDERS)])
        pc.set_alpha(0.7)

    parts["cmeans"].set_color("green")
    parts["cmedians"].set_color("red")
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

    for idx, pos in enumerate(positions):
        mean_val = mean_vals[idx]
        median_val = median_vals[idx]
        plt.text(
            pos + 0.1, mean_val + 0.002, f"{mean_val*100:.2f}%", color="green",
            fontsize=8, ha="left", va="bottom", rotation=30
        )
        plt.text(
            pos + 0.1, median_val - 0.002, f"{median_val*100:.2f}%", color="red",
            fontsize=8, ha="left", va="top", rotation=30
        )

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
        fontsize=12,
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
    get_violin(max_samples=500, diff=False, output="violin_multi_folder.png")