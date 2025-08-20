import os
import csv

# 目录路径
TEST_DIR = 'MMLU-SUB'
CHINESE_DIR = 'MMLU-SUB_chinese'
OUTPUT_DIR = 'MMLU-FILLING'

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

for chinese_filename in os.listdir(CHINESE_DIR):
    if not chinese_filename.endswith('_chinese.csv'):
        continue

    # 找到对应的 input1 文件名
    base_name = chinese_filename.replace('_chinese.csv', '')
    input1_filename = f'{base_name}.csv'

    input1_path = os.path.join(TEST_DIR, input1_filename)
    input2_path = os.path.join(CHINESE_DIR, chinese_filename)
    output_path = os.path.join(OUTPUT_DIR, input1_filename)

    # 检查input1文件是否存在
    if not os.path.exists(input1_path):
        print(f'找不到对应的input1文件: {input1_path}，跳过')
        continue

    # 读取两个CSV文件
    with open(input1_path, 'r', encoding='utf-8') as f1, \
         open(input2_path, 'r', encoding='utf-8') as f2:
        reader1 = list(csv.reader(f1))
        reader2 = list(csv.reader(f2))

    # 建立input1的index到行的映射
    index_to_row1 = {row[0]: row for row in reader1}

    # 合并并写出
    with open(output_path, 'w', newline='', encoding='utf-8') as fout:
        writer = csv.writer(fout)
        for row2 in reader2:
            idx = row2[0]
            if idx not in index_to_row1:
                print(f"警告: input1文件中找不到index {idx}，跳过该行")
                continue
            row1 = index_to_row1[idx]
            new_row = row1[0:6] + row2[1:7]
            writer.writerow(new_row)

    print(f"已合并: {input1_filename} + {chinese_filename} -> {output_path}")

print("全部处理完成。")