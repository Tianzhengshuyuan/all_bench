def append_file_content(source_file, target_file):
    """把 source_file 的内容拼接到 target_file 的结尾"""
    with open(source_file, 'r', encoding='utf-8') as src, \
         open(target_file, 'a', encoding='utf-8') as tgt:
        tgt.write('\n')  # 可选：确保新内容从新一行开始
        for line in src:
            tgt.write(line)

if __name__ == "__main__":
    # 你可以改成自己的文件名
    source = 'log/related_work2_gpt4.1.log'
    target = 'log/related_work_gpt4.1.log'
    append_file_content(source, target)
    print(f"已将 {source} 的内容追加到 {target} 的末尾！")