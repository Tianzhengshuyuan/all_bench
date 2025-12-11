import sys

def move_lines_to_front(file_path, start_line):
    """
    将文件中从 start_line 开始的所有行剪切到开头。
    
    :param file_path: 文件路径
    :param start_line: 起始行号（从 1 开始计数）
    """
    # 读取所有行
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    if start_line < 1 or start_line > len(lines):
        raise ValueError(f"start_line 超出范围 (1 ~ {len(lines)})")

    # 分割
    head = lines[:start_line - 1]   # 起始行之前的部分
    tail = lines[start_line - 1:]   # 从起始行到文件结尾

    # 拼接：tail 放前面，head 放后面
    new_lines = tail + head

    # 写回文件
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python move_lines.py <文件路径> <起始行号>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    start_line = int(sys.argv[2])
    move_lines_to_front(file_path, start_line)
    print(f"已将 {file_path} 从第 {start_line} 行开始的内容移动到文件开头。")