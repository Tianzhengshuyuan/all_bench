import re
from collections import defaultdict
import argparse

# ANSI 颜色定义（控制终端彩色输出）
COLOR_RED = "\033[91m"
COLOR_BLUE = "\033[94m"
COLOR_RESET = "\033[0m"


def analyze_log_grouped(file_path, part=None, auto_part=None):
    """分析日志文件（单轮 + 第二轮题目），可计算前N题的累计准确率，并与总体比较。"""

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # -------------------------
    # 正则模板
    # -------------------------
    question_pattern = re.compile(r'^第(\d+)题 prompt')
    model_answer_pattern = re.compile(r'####(.*?)####')
    correct_answer_pattern = re.compile(r'正确答案:\s*(\S+)')

    group_pattern = re.compile(r'^第(\d+)组 第二轮题目:')
    new_answer_start_pattern = re.compile(r'^[\w\d_]*回答:')
    new_answer_content_pattern = re.compile(r'####(.*?)####')
    new_correct_pattern = re.compile(r'正确答案是:\s*(\S+)')

    # -------------------------
    # 状态变量
    # -------------------------
    current_question = None
    model_answer = None
    correct_answer = None
    in_model_section = False

    current_group = None
    new_answer = None
    new_correct = None
    in_new_answer_section = False

    # -------------------------
    # 统计容器
    # -------------------------
    question_stats = defaultdict(lambda: {'correct': 0, 'total': 0})
    new_question_stats = defaultdict(lambda: {'correct': 0, 'total': 0})

    # -------------------------
    # 主循环
    # -------------------------
    for line in lines:
        line = line.strip()

        # --- 第一轮 ---
        m = question_pattern.search(line)
        if m:
            if current_question and model_answer and correct_answer:
                question_stats[current_question]['total'] += 1
                if model_answer == correct_answer:
                    question_stats[current_question]['correct'] += 1
            current_question = int(m.group(1))
            model_answer = None
            correct_answer = None
            in_model_section = False
            continue

        if line.startswith("模型回答:"):
            m = model_answer_pattern.search(line)
            if m:
                model_answer = m.group(1).strip()
                in_model_section = False
            else:
                in_model_section = True
            continue

        if in_model_section:
            m = model_answer_pattern.search(line)
            if m:
                model_answer = m.group(1).strip()
                in_model_section = False
            continue

        m = correct_answer_pattern.search(line)
        if m:
            correct_answer = m.group(1).strip()
            continue

        # --- 第二轮题目 ---
        g = group_pattern.search(line)
        if g:
            if current_group and new_answer and new_correct:
                qid = (current_group + 1) if current_group < 30 else 1
                new_question_stats[qid]['total'] += 1
                if new_answer == new_correct:
                    new_question_stats[qid]['correct'] += 1
            current_group = int(g.group(1))
            new_answer = None
            new_correct = None
            in_new_answer_section = False
            continue

        if new_answer_start_pattern.search(line):
            m = new_answer_content_pattern.search(line)
            if m:
                new_answer = m.group(1).strip()
                in_new_answer_section = False
            else:
                in_new_answer_section = True
            continue

        if in_new_answer_section:
            m = new_answer_content_pattern.search(line)
            if m:
                new_answer = m.group(1).strip()
                in_new_answer_section = False
            continue

        m = new_correct_pattern.search(line)
        if m:
            new_correct = m.group(1).strip()
            continue

    # --- 收尾 ---
    if current_question and model_answer and correct_answer:
        question_stats[current_question]['total'] += 1
        if model_answer == correct_answer:
            question_stats[current_question]['correct'] += 1

    if current_group and new_answer and new_correct:
        qid = (current_group + 1) if current_group < 30 else 1
        new_question_stats[qid]['total'] += 1
        if new_answer == new_correct:
            new_question_stats[qid]['correct'] += 1

    # -------------------------
    # 每题合并统计
    # -------------------------
    all_ids = sorted(set(question_stats.keys()) | set(new_question_stats.keys()))
    combined_stats = {}

    print("\n=== 合并总体准确率 ===")
    print("题号\t单轮准确率\t多轮准确率\t合并准确率\t合并答对数/样本数")

    for qid in all_ids:
        o_t = question_stats[qid]['total']
        o_c = question_stats[qid]['correct']
        n_t = new_question_stats[qid]['total']
        n_c = new_question_stats[qid]['correct']

        total = o_t + n_t
        correct = o_c + n_c
        acc_o = (o_c / o_t * 100) if o_t else 0
        acc_n = (n_c / n_t * 100) if n_t else 0
        acc_comb = (correct / total * 100) if total else 0

        combined_stats[qid] = {'total': total, 'correct': correct}

        print(f"{qid}\t{acc_o:.2f}\t\t{acc_n:.2f}\t\t{acc_comb:.2f}\t\t({correct}/{total})")

    # -------------------------
    # 总体
    # -------------------------
    total_all = sum(v['total'] for v in question_stats.values())
    correct_all = sum(v['correct'] for v in question_stats.values())
    total_new_all = sum(v['total'] for v in new_question_stats.values())
    correct_new_all = sum(v['correct'] for v in new_question_stats.values())

    total_comb = total_all + total_new_all
    correct_comb = correct_all + correct_new_all
    overall_comb_acc = (correct_comb / total_comb * 100) if total_comb else 0

    print(f"\n总体(合并): {overall_comb_acc:.2f}% ({correct_comb}/{total_comb})\n")

    # -------------------------
    # auto_part: 累计准确率 + 与总体比较
    # -------------------------
    if auto_part and auto_part > 1:
        print(f"=== 前 1~{auto_part} 题累计准确率（对比总体） ===")
        cum_total = 0
        cum_correct = 0

        for qid in all_ids:
            cum_total += combined_stats[qid]['total']
            cum_correct += combined_stats[qid]['correct']

            if qid >= 1 and qid <= auto_part:
                cur_acc = (cum_correct / cum_total * 100) if cum_total else 0
                diff_color = COLOR_RED if cur_acc > overall_comb_acc else COLOR_BLUE
                diff_arrow = "↑" if cur_acc > overall_comb_acc else "↓"
                print(f"前{qid}题累计准确率: {diff_color}{cur_acc:.2f}%{COLOR_RESET} {diff_arrow} "
                      f"(总体: {overall_comb_acc:.2f}%)  ({cum_correct}/{cum_total})")
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="分析日志文件，统计各题及前N题累计准确率（带颜色对比总体）。")
    parser.add_argument("--logfile", type=str, required=True, help="日志文件路径。")
    parser.add_argument("--part", type=int, default=None, help="输出前N题平均准确率。")
    parser.add_argument("--auto_part", type=int, default=None, help="自动打印前2~N题累计准确率。")
    args = parser.parse_args()

    analyze_log_grouped(args.logfile, part=args.part, auto_part=args.auto_part)