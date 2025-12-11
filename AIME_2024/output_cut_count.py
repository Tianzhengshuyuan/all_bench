import re
from collections import Counter

def count_idx_values(log_file):
    # 使用正则表达式匹配 idx=数字 的模式
    pattern = re.compile(r'idx=(\d+)')
    
    counts = Counter()

    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            matches = pattern.findall(line)
            if matches and "kimi" in line:
                for m in matches:
                    num = int(m)
                    if 1 <= num <= 30:
                        counts[num] += 1

    # 输出统计结果
    print("idx 值出现次数统计：")
    for i in range(1, 31):
        print(f"idx={i:<2} : {counts[i]}")

if __name__ == "__main__":
    # 这里替换为你的日志文件名
    count_idx_values("hello.log")