def parse_log_file(file_path):
    first_right = 0
    second_right = 0
    count = 0  # 用来判断奇偶
    
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("kimi回答:"):
            count += 1
            model_answer = line[len("kimi回答:"):].strip()
            
            # 下一行必然是正确答案
            if i + 1 < len(lines):
                next_line = lines[i+1].strip()
                if next_line.startswith("正确答案是:"):
                    correct_answer = next_line[len("正确答案是:"):].strip()
                    
                    # 判断是否正确
                    if correct_answer in model_answer:
                        if count % 2 == 1:  # 奇数
                            print(f"第{(count + 1) // 2}组 第一轮回答正确, 模型答案: {model_answer}, 正确答案: {correct_answer}")
                            first_right += 1
                        else:  # 偶数
                            # print(f"第{count // 2}组 第二轮回答正确, 模型答案: {model_answer}, 正确答案: {correct_answer}")
                            second_right += 1
            i += 2  # 跳过“正确答案是”那一行
        else:
            i += 1
    
    return first_right, second_right


if __name__ == "__main__":
    file_path = "log/test_muiti_turn_kimi.log"  # 替换成你的文件路径
    first_right, second_right = parse_log_file(file_path)
    print("first_right:", first_right)
    print("second_right:", second_right)