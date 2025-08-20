import os
import csv

# 设置你的目标文件夹
folder_path = r'MMLU-TEST'  

for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        temp_path = os.path.join(folder_path, f'temp_{filename}')

        with open(file_path, 'r', newline='', encoding='utf-8') as infile, \
             open(temp_path, 'w', newline='', encoding='utf-8') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            for idx, row in enumerate(reader, start=1):
                writer.writerow([idx] + row)

        # 用处理过的新文件替换原文件
        os.replace(temp_path, file_path)