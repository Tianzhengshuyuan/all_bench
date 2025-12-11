#!/bin/bash

group1=("mistralL" "mistralM" "gpt35" "gpt41")
# 定义第二层循环的数组（数字组）
group2=("filling_english" "filling_english_red" "filling_english_kp1" "filling_english_kp2" "filling_english_kp3" "filling_english_novel")

# 第一层循环：遍历group1
for str in "${group1[@]}"; do
    # 第二层循环：遍历group2
    for num in "${group2[@]}"; do
        # 处理当前组合，示例：打印配对结果
        echo "当前组合: $str - $num"
	    python test_default.py --input dataset/${num}.csv --cot --model=${str} > log/ana_${num}_cot_${str}.log &
	    python test_default.py --input dataset/${num}.csv --model=${str} > log/ana_${num}_${str}.log &
        
        # 可添加具体业务逻辑，例如：
        # command --param1 "$str" --param2 "$num"
    done
    # 每组字符串处理完后可添加分隔线（可选）
    echo "------------------------"
done

echo "所有组合处理完毕"

#python test_default.py --input dataset/filling_english_kp1.csv --cot --model=kimi > log/ana_cot_kimi.log
