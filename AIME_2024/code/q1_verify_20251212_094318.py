inputs = {'y_exponent_denominator': 3, 'x_exponent': 4, 'z_exponent': 2}

from fractions import Fraction

def solve(y_exponent_denominator):
    """
    计算题目中 m+n 的值：
    已知：
      log2(x/(yz)) = 1/2
      log2(y/(xz)) = 1/3
      log2(z/(xy)) = 1/4
    目标：
      |log2(x^x_exp * y^y_exp * z^z_exp)| 的最简分数为 m/n，返回 m+n

    输入参数：
      y_exponent_denominator: int
        - 合理取值范围：整数且 >= 2（保证 z 的指数 y-1 为正）
        - 在题目中对应 y 的指数；其余指数从该值推导：
            x_exp = y_exponent_denominator + 1
            z_exp = y_exponent_denominator - 1
    """
    y_exp = int(y_exponent_denominator)
    if y_exp < 2:
        raise ValueError("y_exponent_denominator should be an integer >= 2")

    # 由主变量推导关联变量（保持 x^4, y^3, z^2 的等差结构）
    x_exp = y_exp + 1
    z_exp = y_exp - 1

    # 设 a = log2(x), b = log2(y), c = log2(z)
    # 方程组：
    # a - b - c = 1/2
    # -a + b - c = 1/3
    # -a - b + c = 1/4
    r1 = Fraction(1, 2)
    r2 = Fraction(1, 3)
    r3 = Fraction(1, 4)

    # 通过成对相加解得：
    # -2a = r2 + r3, -2b = r1 + r3, -2c = r1 + r2
    a = -(r2 + r3) / 2
    b = -(r1 + r3) / 2
    c = -(r1 + r2) / 2

    # 目标值：| x_exp*a + y_exp*b + z_exp*c |
    value = abs(x_exp * a + y_exp * b + z_exp * c)  # Fraction，已最简
    return value.numerator + value.denominator

# 调用 solve
result = solve(inputs['y_exponent_denominator'])
print(result)