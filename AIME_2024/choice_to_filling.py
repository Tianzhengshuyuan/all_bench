import csv
import argparse

def process_csv(input_file: str, output_file: str) -> None:
    """
    读取 input_file，根据第 6 列的正确答案选择对应选项，
    然后写入到 output_file 中（新文件只有两列：题目+正确选项内容）。
    """
    with open(input_file, "r", encoding="utf-8", newline="") as fin, \
         open(output_file, "w", encoding="utf-8", newline="") as fout:

        reader = csv.reader(fin)
        writer = csv.writer(fout)

        for row in reader:
            # 防止列数不足
            if len(row) < 6:
                continue

            question = row[0]        # 第一列保持一致
            answer_flag = row[5].strip()  # 第六列：A/B/C/D

            # 根据答案选择原csv的对应列
            if answer_flag == "A":
                chosen = row[1]
            elif answer_flag == "B":
                chosen = row[2]
            elif answer_flag == "C":
                chosen = row[3]      # 按你给的规则：C -> row[2]
            elif answer_flag == "D":
                chosen = row[4]
            else:
                chosen = ""

            writer.writerow([question, chosen])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="根据原 CSV 第 6 列的正确答案列，抽取对应选项生成新 CSV。")
    parser.add_argument("--input",required=True,help="输入 CSV 文件路径")
    parser.add_argument("--output",required=True,help="输出 CSV 文件路径")

    args = parser.parse_args()
    process_csv(args.input, args.output)