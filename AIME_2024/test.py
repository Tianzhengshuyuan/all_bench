from fractions import Fraction
import math
from math import comb
import sympy as sp
from math import gcd, isqrt

def log_system_mn_sum(X1: int, X2: int, X3: int, Y1: int, Y2: int, Y3: int) -> int:
    """
    解决系统:
        a - b - c = Y1
        b - a - c = Y2
        c - a - b = Y3
    然后计算 |a/X1 + b/X2 + c/X3| = m/n ，返回 m + n。
    全程保持分数形式。
    """
    # 保持为分数形式
    Y1, Y2, Y3 = Fraction(Y1), Fraction(Y2), Fraction(Y3)
    X1, X2, X3 = Fraction(X1), Fraction(X2), Fraction(X3)

    # 方程组解
    a = (Y2 + Y3) / Fraction(-2)
    b = (Y1 + Y3) / Fraction(-2)
    c = (Y1 + Y2) / Fraction(-2)

    # 计算表达式（使用分数除法）
    val = abs(a / X1 + b / X2 + c / X3)

    # 化为既约分数
    val = val.limit_denominator()
    m, n = val.numerator, val.denominator

    return m + n
if __name__ == "__main__":
    print(log_system_mn_sum(2, 3, 5, 1, 2, 3))
