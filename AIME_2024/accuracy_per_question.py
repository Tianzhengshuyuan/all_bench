import re
from collections import defaultdict
import argparse

# ANSI 颜色定义
COLOR_RED = "\033[91m"
COLOR_BLUE = "\033[94m"
COLOR_GRAY = "\033[90m"
COLOR_RESET = "\033[0m"

def analyze_log_grouped(file_path, part=None, auto_part=False):
    """
    分析日志文件，统计每道题的平均准确率。
    支持：
      - --part: 打印前 N 题平均准确率
      - --auto_part: 自动打印前2~20题平均准确率，对比总体并彩色显示
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 正则模板
    question_pattern = re.compile(r'^第(\d+)题 prompt')
    model_answer_pattern = re.compile(r'####(.*?)####')
    correct_answer_pattern = re.compile(r'正确答案:\s*(\S+)')

    # 状态变量
    current_question = None
    model_answer = None
    correct_answer = None
    in_model_section = False

    # 每题统计
    question_stats = defaultdict(lambda: {'correct': 0, 'total': 0})

    # -------------------------
    # 主逻辑
    # -------------------------
    for line in lines:
        line = line.strip()

        # 匹配题号
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

        # 模型回答
        if line.startswith("模型回答:"):
            m = model_answer_pattern.search(line)
            if m:
                model_answer = m.group(1).strip()
                in_model_section = False
            else:
                in_model_section = True
            continue

        # 如果在模型回答段落中
        if in_model_section:
            m = model_answer_pattern.search(line)
            if m:
                model_answer = m.group(1).strip()
                in_model_section = False
            continue

        # 正确答案
        m = correct_answer_pattern.search(line)
        if m:
            correct_answer = m.group(1).strip()
            continue

    # 处理最后一题
    if current_question and model_answer and correct_answer:
        question_stats[current_question]['total'] += 1
        if model_answer == correct_answer:
            question_stats[current_question]['correct'] += 1

    # -------------------------
    # 输出每题统计
    # -------------------------
    print("题号\t样本数\t答对数\t准确率(%)")
    sorted_ids = sorted(question_stats.keys())
    for qid in sorted_ids:
        total = question_stats[qid]['total']
        correct = question_stats[qid]['correct']
        acc = (correct / total * 100) if total > 0 else 0
        print(f"{qid}\t{total}\t{correct}\t{acc:.2f}")

    # -------------------------
    # 总体准确率
    # -------------------------
    total_all = sum(v['total'] for v in question_stats.values())
    correct_all = sum(v['correct'] for v in question_stats.values())
    overall_acc = (correct_all / total_all * 100) if total_all > 0 else 0
    print(f"\n总体: {correct_all}/{total_all} = {overall_acc:.2f}%")

    # -------------------------
    # part 参数
    # -------------------------
    if part is not None:
        selected = [qid for qid in sorted_ids if qid <= part]
        if selected:
            total_sel = sum(question_stats[qid]['total'] for qid in selected)
            correct_sel = sum(question_stats[qid]['correct'] for qid in selected)
            acc_sel = (correct_sel / total_sel * 100) if total_sel > 0 else 0
            print(f"前{part}题平均准确率: {acc_sel:.2f}% ({correct_sel}/{total_sel})")
        else:
            print(f"警告：日志中未检测到编号 ≤ {part} 的题目。")

    # -------------------------
    # auto_part 参数（自动分析 2~20题）
    # -------------------------
    if auto_part:
        print("\n自动分析（前2~20题平均准确率对比）:")
        print("题数\t样本数\t答对数\t前N题准确率(%)\t总体准确率(%)\t对比关系")

        for n in range(2, 29):
            selected = [qid for qid in sorted_ids if qid <= n]
            if not selected:
                continue
            total_sel = sum(question_stats[qid]['total'] for qid in selected)
            correct_sel = sum(question_stats[qid]['correct'] for qid in selected)
            acc_sel = (correct_sel / total_sel * 100) if total_sel > 0 else 0

            # 对比关系 + 颜色
            if acc_sel > overall_acc + 1e-9:
                relation_text = "高于总体"
                color = COLOR_RED
            elif acc_sel < overall_acc - 1e-9:
                relation_text = "低于总体"
                color = COLOR_BLUE
            else:
                relation_text = "相同"
                color = COLOR_GRAY

            relation_colored = f"{color}{relation_text}{COLOR_RESET}"

            print(f"{n}\t{total_sel}\t{correct_sel}\t{acc_sel:.2f}\t\t{overall_acc:.2f}\t\t{relation_colored}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="分析日志文件，统计各题准确率。")
    parser.add_argument("--logfile", type=str, required=True, help="日志文件路径。")
    parser.add_argument("--part", type=int, default=None,
                        help="若指定该参数，则输出前N题的平均准确率。")
    parser.add_argument("--auto_part", action="store_true",
                        help="若设置，则自动打印前2~20题平均准确率，并与总体进行比较。")
    args = parser.parse_args()

    analyze_log_grouped(args.logfile, part=args.part, auto_part=args.auto_part)