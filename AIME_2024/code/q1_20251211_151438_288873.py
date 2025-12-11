inputs = {'eq3_rhs_denominator': 6}

from fractions import Fraction

def solve(eq3_rhs_denominator):
    """
    求解 |log2(x^4 y^3 z^2)| = m/n 的 m+n。
    输入参数:
        eq3_rhs_denominator: 第三条方程右侧的分母 d，满足 log2(z/(xy)) = 1/d
    合理取值范围:
        d 为正整数 (d >= 1)
    """
    d = int(eq3_rhs_denominator)
    if d <= 0:
        raise ValueError("eq3_rhs_denominator must be a positive integer (>=1).")

    # 定义三条方程右端常量
    r1 = Fraction(1, 2)  # log2(x/(yz)) = 1/2
    r2 = Fraction(1, 3)  # log2(y/(xz)) = 1/3
    r3 = Fraction(1, d)  # log2(z/(xy)) = 1/d

    # 设 a=log2(x), b=log2(y), c=log2(z)
    # 由两两相加可得：
    # -2a = r2 + r3, -2b = r1 + r3, -2c = r1 + r2
    a = -(r2 + r3) / 2
    b = -(r1 + r3) / 2
    c = -(r1 + r2) / 2

    # 目标值：|4a + 3b + 2c|
    S_abs = abs(4 * a + 3 * b + 2 * c)  # 为最简分数
    m, n = S_abs.numerator, S_abs.denominator
    return m + n

# 调用 solve
result = solve(inputs['eq3_rhs_denominator'])
print(result)