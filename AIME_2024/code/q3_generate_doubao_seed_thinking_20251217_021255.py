inputs = {None: 4}

import math

def solve(_):
    # 计算大奖的情况数（4个全对）
    grand = math.comb(4, 4) * math.comb(6, 0)
    # 计算对2个的情况数
    two_correct = math.comb(4, 2) * math.comb(6, 2)
    # 计算对3个的情况数
    three_correct = math.comb(4, 3) * math.comb(6, 1)
    # 中奖的总情况数（至少2个正确）
    total_prize = two_correct + three_correct + grand
    # 条件概率的分子（大奖）和分母（中奖）
    numerator = grand
    denominator = total_prize
    # 约分
    common_divisor = math.gcd(numerator, denominator)
    m = numerator // common_divisor
    n = denominator // common_divisor
    # 返回m + n
    return m + n

# 调用 solve
result = solve(inputs)
print(result)