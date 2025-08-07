import argparse
import csv
import sys

def main():
    parser = argparse.ArgumentParser(description="合并两个CSV文件的指定列")
    parser.add_argument('--input1', required=True, help="第一个输入CSV文件路径")
    parser.add_argument('--input2', required=True, help="第二个输入CSV文件路径")
    parser.add_argument('--output', required=True, help="输出CSV文件路径")
    args = parser.parse_args()

    # 读取两个CSV文件
    with open(args.input1, 'r', encoding='utf-8') as f1, \
         open(args.input2, 'r', encoding='utf-8') as f2:
        reader1 = list(csv.reader(f1))
        reader2 = list(csv.reader(f2))

    # 检查行数
    if len(reader1) != len(reader2):
        print(f"错误：{args.input1} 和 {args.input2} 的行数不同！({len(reader1)} vs {len(reader2)})")
        sys.exit(1)

    # 合并并写出
    with open(args.output, 'w', newline='', encoding='utf-8') as fout:
        writer = csv.writer(fout)
        for row1, row2 in zip(reader1, reader2):
            # 取input1第一列，input2第2~6列
            new_row = [row1[0]] + row2[1:6]
            writer.writerow(new_row)

if __name__ == "__main__":
    main()