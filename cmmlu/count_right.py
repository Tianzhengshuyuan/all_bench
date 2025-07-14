import re

def process_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    stat_pattern = re.compile(r'总题数:\s*(\d+),\s*正确答案数:\s*(\d+),\s*正确率:\s*([\d.]+)%,\s*耗时:\s*([\d.]+)秒')
    stat_indices = []
    # 记录所有统计行的索引
    for idx, line in enumerate(lines):
        if stat_pattern.search(line):
            stat_indices.append(idx)
    # 加上边界，方便处理
    stat_indices = [-1] + stat_indices

    for i in range(1, len(stat_indices)):
        group_start = stat_indices[i-1] + 1
        group_end = stat_indices[i]  # 不包含统计行
        # 收集本组题目区间
        group_lines = lines[group_start:group_end]
        # 找deepseek答案和正确答案
        selected = []
        correct = []
        for line in group_lines:
            m = re.search(r'####([A-D])####', line)
            if m:
                selected.append(m.group(1))
            c = re.search(r'正确答案是:\s*([A-D])', line)
            if c:
                correct.append(c.group(1))
        # 按顺序比较
        correct_cnt = sum([1 for x, y in zip(selected, correct) if x == y])
        total_cnt = len(correct)
        # 替换对应统计行
        stat_idx = stat_indices[i]
        line = lines[stat_idx]
        m = stat_pattern.search(line)
        if m:
            new_line = f"总题数: {m.group(1)}, 正确答案数: {correct_cnt}, 正确率: {correct_cnt / int(m.group(1)) * 100:.2f}%, 耗时: {m.group(4)}秒\n"
            lines[stat_idx] = new_line

    # 写回文件
    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(lines)

if __name__ == "__main__":
    process_file("log/test_origin_kimi.log")  # 替换为你的文件名