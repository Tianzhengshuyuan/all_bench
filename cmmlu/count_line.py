import os
import csv

# 文件夹路径
test_folder = './test'
test_french_folder = './test_french'

for french_filename in os.listdir(test_french_folder):
    if french_filename.endswith('.csv'):
        french_filepath = os.path.join(test_french_folder, french_filename)
        
        # 推断对应的test文件名
        if french_filename.endswith('_french.csv'):
            base_name = french_filename[:-11]  # 去掉"_french.csv"
            test_filename = base_name + '.csv'
        else:
            continue
        
        test_filepath = os.path.join(test_folder, test_filename)
        
        # 检查test文件是否存在
        if not os.path.exists(test_filepath):
            print(f"Test file not found for: {french_filename}")
            continue
        
        # 统计french文件的csv行数
        with open(french_filepath, 'r', encoding='utf-8') as f_french:
            french_reader = csv.reader(f_french)
            french_rows = sum(1 for row in french_reader)
        
        # 统计test文件的csv行数
        with open(test_filepath, 'r', encoding='utf-8') as f_test:
            test_reader = csv.reader(f_test)
            test_rows = sum(1 for row in test_reader)
        
        # 判断行数是否一致
        if french_rows != test_rows:
            print(f'文件行数不同: {french_filename} ({french_rows}行) <-> {test_filename} ({test_rows}行)')