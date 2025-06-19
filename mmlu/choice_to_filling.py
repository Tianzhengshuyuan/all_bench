import csv
import argparse
import os
from fractions import Fraction

def is_number_or_fraction(s):
    s = s.strip()
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        Fraction(s)
        return True
    except Exception:
        return False

def filter_question(row):
    if len(row) < 5:
        return False
    for i in range(1, 5):
        cell = str(row[i]).strip()
        # 直接为单个数字或分数
        if is_number_or_fraction(cell):
            continue
        # 逗号分隔的多个数字或分数
        parts = cell.split(',')
        if len(parts) > 1 and all(is_number_or_fraction(p) for p in parts):
            continue
        return False
    return True

def choice_to_filling():
    # 读取csv文件
    with open(args.input, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    # 答案对应的选项列索引
    answer_to_col = {'A': 1, 'B': 2, 'C': 3, 'D': 4}

    # 新的结果列表
    output_rows = []

    for row in rows:
        if not filter_question(row):
            continue
        question = row[0]
        answer = str(row[5]).strip() if len(row) > 5 else ''
        answer_col = answer_to_col.get(answer)
        if answer_col is not None and len(row) > answer_col:
            correct = row[answer_col]
            output_rows.append([question, correct])

    # 自动生成输出文件名
    base = os.path.splitext(os.path.basename(args.input))[0]
    output_file = f"{base}_filling.csv"

    # 写入结果
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(output_rows)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help="输入 CSV 文件名")
    args = parser.parse_args()

    choice_to_filling()