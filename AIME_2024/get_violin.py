import os
import re
import ast
import argparse
import numpy as np
import matplotlib.pyplot as plt

# ----------------------
# 正则模式定义
# ----------------------
pattern1 = re.compile(
    r"总题组数:\s*\d+.*?第一轮正确答案数:\s*\d+.*?正确率:\s*[\d.]+%.*?第二轮正确答案数:\s*\d+.*?正确率:\s*([\d.]+)%",
    re.DOTALL,
)
pattern2 = re.compile(
    r"总题数:\s*\d+.*?正确数:\s*\d+.*?正确率:\s*([\d.]+)%,\s*耗时:", re.DOTALL
)

# =====================================================================
# get_key_accuracies —— 解析 key→accuracy，并解析完整配置
# =====================================================================
def get_key_accuracies(logfile, folder_name):
    config_pattern_serial = re.compile(r"处理key: (\d+),\s*配置:\s*(\{.*\})", re.DOTALL)
    config_pattern_parallel = re.compile(r"配置\s*key=(\d+),\s*配置\s*=\s*(\{.*\})", re.DOTALL)

    key_acc_map = {}
    skipped_tokens10 = 0
    skipped_temperature2 = 0
    skipped_out_of_range = 0
    skipped_parse_error = 0

    current_key = None
    current_cfg = None

    with open(logfile, "r", encoding="utf-8") as f:
        for line in f:
            # ---- Step 1: 匹配配置行 ----
            if args.parallel:
                m_cfg = config_pattern_parallel.search(line) 
            else:
                m_cfg = config_pattern_serial.search(line)
            if m_cfg:
                current_key = int(m_cfg.group(1))
                cfg_str = m_cfg.group(2)
                try:
                    current_cfg = ast.literal_eval(cfg_str)
                except Exception:
                    current_cfg = None
                    skipped_parse_error += 1
                continue

            # ---- Step 2: 匹配 accuracy ----
            m1 = pattern1.search(line)
            m2 = pattern2.search(line)
            acc = None
            if m1:
                acc = float(m1.group(1)) / 100.0
            elif m2:
                acc = float(m2.group(1)) / 100.0

            # ---- Step 3: 保存结果（加过滤）----
            if acc is not None and current_key is not None:
                # 获取配置中的 max_tokens 值

                max_tokens = current_cfg['max_tokens']
                temperature = current_cfg['Temperature']
                cot = current_cfg.get('cot', False)
                if args.max_samples is not None and current_key >= args.max_samples:
                    skipped_out_of_range += 1
                # elif max_tokens == 10:
                #     skipped_tokens10 += 1
                #     # print("跳过 max_tokens=10的记录")
                # elif temperature == 2.0:
                #     skipped_temperature2 += 1
                #     # print("跳过 temperature=2.0 的记录")
                else:
                    key_acc_map[current_key] = acc

                current_key = None
                current_cfg = None

    # 报告
    if (skipped_tokens10 + skipped_out_of_range + skipped_parse_error) > 0:
        print(
            f"[{os.path.basename(logfile)}] skipped: "
            f"max_tokens=10 → {skipped_tokens10}, "
            f"out_of_range → {skipped_out_of_range}, "
            f"parse_error → {skipped_parse_error}"
        )

    return key_acc_map


# =====================================================================
# label 美化映射
# =====================================================================
def prettify_labels(labels):
    mapping = {
        "deepseekv3": "deepseek-v3",
        "doubao": "doubao-1.5-pro",
        "gpt35": "gpt-3.5",
        "gpt41": "gpt-4.1",
        "kimiv1": "moonshot-v1-8k",
        "mistralL": "mistral-large",
        "mistralM": "mistral-medium",
        "qwen": "qwen-plus",
        "qwen25": "qwen2.5-32b",
    }
    return [mapping.get(lbl, lbl) for lbl in labels]


# =====================================================================
# 生成小提琴图
# =====================================================================
def get_violin():
    # target_labels = ["deepseekv3", "doubao", "kimiv1", "qwen25"]
    target_labels = ["deepseekv3", "doubao", "gpt35", "gpt41", "kimiv1", "mistralL", "mistralM", "qwen", "qwen25"]
    label2accs = {lbl: [] for lbl in target_labels}

    all_files = [f for f in os.listdir(args.input_folder) if f.endswith(".log")]
    all_files.sort()


    for filename in all_files:
        matched_label = None
        for lbl in target_labels:
            if args.parallel:
                if f"_{lbl}_" in filename:
                    matched_label = lbl
                    break
            else:
                if filename.startswith(f"sample_test_{lbl}."):
                    matched_label = lbl
                    break
        if matched_label is None:
            continue

        filepath = os.path.join(args.input_folder, filename)
        key_acc_dict = get_key_accuracies(filepath, folder_name=args.input_folder)
        if not key_acc_dict:
            print(f"⚠️ 文件 {filename} 中未找到有效准确率数据，跳过。")
            continue

        sorted_keys = sorted(key_acc_dict.keys())
        accuracies = np.array([key_acc_dict[k] for k in sorted_keys], dtype=float)
        label2accs[matched_label].extend(accuracies.tolist())
        print(f"读取 {filename}: {len(accuracies)} 条记录 -> 累计 {len(label2accs[matched_label])} 条")

    valid_labels = [lbl for lbl, accs in label2accs.items() if len(accs) > 0]
    if not valid_labels:
        print("❌ 没有找到匹配数据，无法绘制。")
        return

    data = [np.array(label2accs[lbl]) for lbl in valid_labels]
    labels = valid_labels

    # 计算每个模型的 mean，用于数值标注
    means = [np.mean(d) for d in data]

    # 计算并打印每个 label 的最大值
    print("\n" + "=" * 60)
    print("各模型准确率最大值统计:")
    print("=" * 60)
    max_values = [np.max(d) for d in data]
    for lbl, max_val in zip(labels, max_values):
        pretty_lbl = prettify_labels([lbl])[0]
        print(f"  {pretty_lbl:20s}: {max_val:.4f}")
    print("=" * 60 + "\n")

    # 绘制小提琴图
    plt.figure(figsize=(10, 6))
    parts = plt.violinplot(
        data, widths=0.6, showmeans=True, showmedians=True, showextrema=True
    )

    # 美化样式
    parts["cmeans"].set_color("#ea6864")
    parts["cmedians"].set_color("#519aba")
    parts["cmaxes"].set_color("#555555")
    parts["cmins"].set_color("#555555")
    parts["cbars"].set_color("#555555")
    for pc in parts["bodies"]:
        pc.set_facecolor("#9975a6")
        pc.set_alpha(0.7)

    # 图例（不变）
    mean_handle = plt.Line2D([0], [0], color="#ea6864", lw=2, label="Mean")
    median_handle = plt.Line2D([0], [0], color="#519aba", lw=2, label="Median")
    plt.legend(handles=[mean_handle, median_handle], fontsize=12)

    # x 轴
    plt.xticks(
        np.arange(1, len(labels) + 1),
        prettify_labels(labels),
        fontsize=14,
        rotation=30,
        ha="right",
    )
    plt.ylabel("Accuracy", fontsize=16)
    plt.xlabel("LLM", fontsize=16)
    plt.yticks(fontsize=14)
    plt.grid(axis="y", linestyle="--", alpha=0.6)

    # ===== 在 mean 点旁边标注具体数值 =====
    # violinplot 的 x 位置与 xticks 一致：1, 2, ..., len(labels)
    # for i, mean_val in enumerate(means, start=1):
    #     # y 位置为 mean 值稍微上方一点，避免与 mean 线重叠
    #     plt.text(
    #         i,
    #         mean_val + 0.01,               # 你可以根据数据范围适当调整偏移量 0.01
    #         f"{mean_val:.3f}",             # 保留三位小数
    #         ha="center",
    #         va="bottom",
    #         fontsize=10,
    #         color="#ea6864",
    #     )

    plt.tight_layout()

    output_file = f"violin_{args.output}"
    plt.savefig(output_file, dpi=300)
    plt.show()
    print(f"✅ 小提琴图已绘制并保存至 {output_file}")


# =====================================================================
# Main
# =====================================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="提取准确率并绘制小提琴图")
    parser.add_argument("--input_folder", default="ames_result_origin", help="日志文件夹路径")
    parser.add_argument("--max_samples", type=int, default=500, help="保留 key 范围（0 ~ max_samples-1）")
    parser.add_argument("--output", default="mes.png", help="输出图像文件名")
    parser.add_argument("--parallel", action="store_true")
    args = parser.parse_args()

    get_violin()