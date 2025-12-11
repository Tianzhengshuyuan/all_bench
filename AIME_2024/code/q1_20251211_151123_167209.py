inputs = {'log_base': 2, 'eq1_rhs_numerator': 1, 'eq1_rhs_denominator': 2, 'eq2_rhs_numerator': 1, 'eq2_rhs_denominator': 3, 'eq3_rhs_numerator': 1, 'eq3_rhs_denominator': 4, 'target_exp_x': 4, 'target_exp_y': 3, 'target_exp_z': 2}

from fractions import Fraction

def solve(target_exp_y):
    """
    计算题目答案 m+n，其中 |log2(x^4 * y^{target_exp_y} * z^2)| = m/n（最简分数），返回 m+n。
    输入参数:
        target_exp_y: int
            合理取值范围：整数（例如 -10^6 到 10^6），题目中为 3。
    """
    # 固定方程右侧常量（题目给定）
    r1 = Fraction(1, 2)  # log2(x/(yz))
    r2 = Fraction(1, 3)  # log2(y/(xz))
    r3 = Fraction(1, 4)  # log2(z/(xy))

    # 设 a=log2(x), b=log2(y), c=log2(z)
    # 由方程组:
    # a - b - c = r1
    # -a + b - c = r2
    # -a - b + c = r3
    # 两两相加可得：
    a = -(r2 + r3) / 2
    b = -(r1 + r3) / 2
    c = -(r1 + r2) / 2

    # 计算 |4a + target_exp_y*b + 2c|
    kx = Fraction(4, 1)
    ky = Fraction(target_exp_y, 1)
    kz = Fraction(2, 1)
    value = abs(kx * a + ky * b + kz * c)

    m, n = value.numerator, value.denominator
    return m + n

# 调用 solve
result = solve(inputs['target_exp_y'])
print(result)