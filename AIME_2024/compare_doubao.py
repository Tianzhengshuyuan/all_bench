import os
import re
import argparse
import numpy as np
import matplotlib.pyplot as plt

# === 正则匹配规则 ===
pattern1 = re.compile(
    r"总题组数:\s*\d+.*?第一轮正确答案数:\s*\d+.*?正确率:\s*[\d.]+%.*?"
    r"第二轮正确答案数:\s*\d+.*?正确率:\s*([\d.]+)%"
)
pattern2 = re.compile(
    r"总题数:\s*\d+.*?正确数:\s*\d+.*?正确率:\s*([\d.]+)%,\s*耗时:"
)
config_pattern_default = re.compile(r"配置 key=(\d+),\s*配置=.*")
config_pattern_log = re.compile(r"处理key:\s*(\d+),\s*配置:\s*\{.*?\}")

# === 提取单个日志中的 key→accuracy 映射 ===
def parse_accuracy_from_log(log_path, folder):
    if folder == "log":
        cfg_pattern = config_pattern_log
    else:
        cfg_pattern = config_pattern_default

    result = {}
    current_key = None
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            m_cfg = cfg_pattern.search(line)
            if m_cfg:
                current_key = int(m_cfg.group(1))
                continue
            m1 = pattern1.search(line)
            m2 = pattern2.search(line)
            acc = None
            if m1:
                acc = float(m1.group(1)) / 100.0
            elif m2:
                acc = float(m2.group(1)) / 100.0
            if acc is not None and current_key is not None:
                result[current_key] = acc
                current_key = None
    return result


# === 主逻辑 ===
folders = ["log", "ames_result_origin"]
# label = "doubao"
data = {}

def compare_accuracies():
    """对比不同文件夹中相同 key 的 accuracy。"""
    for folder in folders:
        files = [f for f in os.listdir(folder)
                if f.startswith("sample_test_") and f.endswith(".log") and args.label in f]
        if not files:
            print(f"[WARN] {folder} 中未找到 {args.label} 日志文件。")
            continue

        all_data = {}
        for f in files:
            path = os.path.join(folder, f)
            parsed = parse_accuracy_from_log(path, folder)
            all_data.update(parsed)
        data[folder] = all_data
        print(f"[INFO] {folder} 提取到 {len(all_data)} 个 key。")


    # === 计算结果 ===
    keys = list(range(args.start,args.end))
    acc_log = [data.get("log", {}).get(k, None) for k in keys]
    acc_origin = [data.get("ames_result_origin", {}).get(k, None) for k in keys]

    smaller = equal = greater = 0
    log_vals, origin_vals = [], []

    for a_log, a_ori in zip(acc_log, acc_origin):
        if a_log is None or a_ori is None:
            continue
        log_vals.append(a_log)
        origin_vals.append(a_ori)
        if a_log < a_ori:
            smaller += 1
        elif abs(a_log - a_ori) < 1e-8:
            equal += 1
        else:
            greater += 1

    # === 打印对比统计 ===
    print("\n=== 🔍 比较统计结果 ===")
    print(f"红点 < 蓝点: {smaller} 个")
    print(f"红点 = 蓝点: {equal} 个")
    print(f"红点 > 蓝点: {greater} 个")

    # === 打印统计指标 ===
    if log_vals:
        mean_log = np.mean(log_vals) * 100
        median_log = np.median(log_vals) * 100
    else:
        mean_log = median_log = float('nan')

    if origin_vals:
        mean_origin = np.mean(origin_vals) * 100
        median_origin = np.median(origin_vals) * 100
    else:
        mean_origin = median_origin = float('nan')

    print("\n=== 📊 准确率统计 ===")
    print(f"红点 (log): 平均值 = {mean_log:.2f}%   中位数 = {median_log:.2f}%")
    print(f"蓝点 (ames_result_origin): 平均值 = {mean_origin:.2f}%   中位数 = {median_origin:.2f}%")

    # === 绘制散点图 ===
    plt.figure(figsize=(14, 6))
    for k, a_log, a_ori in zip(keys, acc_log, acc_origin):
        if a_log is not None:
            plt.scatter(k, a_log * 100, color="red", s=36, label="log" if k == 0 else "")
        if a_ori is not None:
            plt.scatter(k, a_ori * 100, color="blue", s=12, label="ames_result_origin" if k == 0 else "")

    plt.xlabel("Config Key (0–499)", fontsize=14)
    plt.ylabel("Accuracy (%)", fontsize=14)
    plt.title(f"{args.label} Accuracy Comparison per Config", fontsize=16)
    plt.legend(fontsize=12)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{args.label}_accuracy_comparison_per_key.png", dpi=300)
    plt.show()

    print(f"\n✅ 散点图已保存为 {args.label}_accuracy_comparison_per_key.png")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="比较不同文件夹中相同 key 的 accuracy。")
    parser.add_argument("--label", type=str, default="doubao", help="日志文件中包含的标签，用于过滤文件。")
    parser.add_argument("--start", type=int, default=0, help="起始 key")
    parser.add_argument("--end", type=int, default=500, help="结束 key")
    args = parser.parse_args()
    compare_accuracies()