import argparse
def truncate_file_from_line(filename, start_line):
    """
    从start_line开始删除文件后面的所有内容（start_line从0开始计数）
    """
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    # 保留前start_line行
    new_lines = lines[:start_line]
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove lines from a file starting from a specific line number.")
    parser.add_argument('--filename', type=str, help='The name of the file to truncate.')
    parser.add_argument('--start_line', type=int, help='The line number from which to start truncating (0-based index).')
    args = parser.parse_args()
    truncate_file_from_line(args.filename, args.start_line)