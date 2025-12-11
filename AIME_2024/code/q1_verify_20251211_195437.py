inputs = {'log_base': 2, 'eq1_rhs_numerator': 1, 'eq1_rhs_denominator': 2, 'eq2_rhs_numerator': 1, 'eq2_rhs_denominator': 3, 'eq3_rhs_numerator': 1, 'eq3_rhs_denominator': 4, 'exp_x_in_target': 4, 'exp_y_in_target': 3, 'exp_z_in_target': 2}

from fractions import Fraction

def solve(exp_z_in_target):
    """
    计算 |log2(x^4 * y^3 * z^exp_z_in_target)| 的最简分数 m/n 的 m+n
    已知:
      log2(x/(yz)) = 1/2
      log2(y/(xz)) = 1/3
      log2(z/(xy)) = 1/4
    其中 a=log2(x), b=log2(y), c=log2(z)
    
    输入参数:
      exp_z_in_target: 目标表达式中 z 的指数
      合理取值范围: 任意整数（可为负，表示 z 的负幂），如 ..., -2, -1, 0, 1, 2, ...
    """
    r1 = Fraction(1, 2)
    r2 = Fraction(1, 3)
    r3 = Fraction(1, 4)
    
    # 由方程组：
    # a - b - c = r1
    # -a + b - c = r2
    # -a - b + c = r3
    # 成对相加可得：
    # -2c = r1 + r2  => c = -(r1 + r2)/2
    # -2a = r2 + r3  => a = -(r2 + r3)/2
    # -2b = r1 + r3  => b = -(r1 + r3)/2
    a = -(r2 + r3) / 2
    b = -(r1 + r3) / 2
    c = -(r1 + r2) / 2

    exp_z = Fraction(exp_z_in_target, 1)
    value = abs(4 * a + 3 * b + exp_z * c)  # |log2(x^4 y^3 z^{exp_z})|
    
    return value.numerator + value.denominator

# 调用 solve
result = solve(inputs['exp_z_in_target'])
print(result)