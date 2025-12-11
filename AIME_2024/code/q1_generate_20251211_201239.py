inputs = {'exp_x': 915501}

from fractions import Fraction

def solve(exp_x):
    """
    计算 |log2(x^exp_x * y^3 * z^2)| = m/n 的 m+n，其中
    x, y, z 为正实数，满足：
        log2(x/(yz)) = 1/2
        log2(y/(xz)) = 1/3
        log2(z/(xy)) = 1/4

    参数:
        exp_x (int): x 的指数。合理取值范围：整数 >= 0（通常小于 10^6 以避免无意义的大数）。
                     也可为较小负整数，但本题设定非负更合理。

    返回:
        int: 分数 m/n 的 m+n
    """
    # 右端常数项（以分数避免精度误差）
    r1 = Fraction(1, 2)
    r2 = Fraction(1, 3)
    r3 = Fraction(1, 4)

    # 令 a = log2(x), b = log2(y), c = log2(z)
    # 方程组：
    # a - b - c = r1
    # -a + b - c = r2
    # -a - b + c = r3
    #
    # 成对相加可得：
    # -2c = r1 + r2  => c = -(r1 + r2)/2
    # -2a = r2 + r3  => a = -(r2 + r3)/2
    # -2b = r1 + r3  => b = -(r1 + r3)/2
    a = -(r2 + r3) / 2
    b = -(r1 + r3) / 2
    c = -(r1 + r2) / 2

    # 目标：|exp_x * a + 3 * b + 2 * c|
    exp_y = 3
    exp_z = 2
    val = abs(Fraction(exp_x) * a + Fraction(exp_y) * b + Fraction(exp_z) * c)

    # 化为既约分数 m/n，返回 m+n
    return val.numerator + val.denominator

# 调用 solve
result = solve(inputs['exp_x'])
print(result)