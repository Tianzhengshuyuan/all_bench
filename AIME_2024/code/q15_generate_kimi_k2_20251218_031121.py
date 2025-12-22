inputs = {'n': 907}

from math import comb

def solve(n):
    # 路径总长度 2n，其中 n 个 R 和 n 个 U
    # 要求恰好 4 次转向，即 5 段
    # 两种对称情况：以 U 开头或以 R 开头
    # 每种情况：3 段一种方向，2 段另一种方向
    # 用 stars and bars 把 n 拆成 3 份正整数：C(n-1, 2)
    # 把 n 拆成 2 份正整数：C(n-1, 1)
    # 两种对称情况，乘以 2
    return 2 * comb(n - 1, 2) * comb(n - 1, 1)

# 对于 8×8 网格，n=8
# print(solve(8))  # 294

# 调用 solve
result = solve(inputs['n'])
print(result)