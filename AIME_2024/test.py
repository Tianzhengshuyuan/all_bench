from fractions import Fraction
import math
from math import comb
import sympy as sp
from math import gcd, isqrt

# === 26 ===
def solve_triangle_symmedian(AB, BC, AC):
    # Apollonius 定理求 AM
    AM = math.sqrt((2 * AB**2 + 2 * AC**2 - BC**2) / 4)

    # 根据相似比求 AP
    AP = (AB * AC) / AM

    # 化为最简分数形式
    frac = Fraction(AP).limit_denominator(10000)

    return frac.numerator + frac.denominator
if __name__ == "__main__":
    print(solve_triangle_symmedian(5, 13, 10))
