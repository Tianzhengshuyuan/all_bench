import os

def remove_first_line_from_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if len(lines) <= 1:
        # 空文件或只有一行，直接清空
        new_lines = []
    else:
        new_lines = lines[1:]
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

def batch_remove_first_line(csv_dir):
    for filename in os.listdir(csv_dir):
        if filename.lower().endswith('.csv'):
            file_path = os.path.join(csv_dir, filename)
            if os.path.isfile(file_path):
                print(f'处理 {file_path} ...')
                remove_first_line_from_csv(file_path)
    print('所有csv文件的第一行已删除。')

if __name__ == "__main__":
    dir_path = input("请输入待处理的文件夹路径：").strip()
    batch_remove_first_line(dir_path)