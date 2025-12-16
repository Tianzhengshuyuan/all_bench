from fractions import Fraction
import sympy as sp
import re
from math import comb
import math
import argparse
def unique_point_on_AB(t: int, z: int, s: int, y: int) -> int:
    """
    计算: ((t/z)^6 + (√s/y)^6) / ((t/z)^2 + (√s/y)^2)^2
    返回最简分数的分子+分母
    """
    # 保持分数，不出现浮点运算
    t_frac = Fraction(t)
    z_frac = Fraction(z)
    s_frac = Fraction(s)
    y_frac = Fraction(y)
    
    # 计算 (t/z)^6
    tz_6 = (t_frac / z_frac) ** 6
    
    # 计算 (√s/y)^6 = (s^(1/2)/y)^6 = s^3 / y^6
    sqrt_s_y_6 = (s_frac ** 3) / (y_frac ** 6)
    
    # 分子: (t/z)^6 + (√s/y)^6
    numerator = tz_6 + sqrt_s_y_6
    
    # 计算 (t/z)^2
    tz_2 = (t_frac / z_frac) ** 2
    
    # 计算 (√s/y)^2 = s / y^2
    sqrt_s_y_2 = s_frac / (y_frac ** 2)
    
    # 分母: ((t/z)^2 + (√s/y)^2)^2
    denominator = (tz_2 + sqrt_s_y_2) ** 2
    
    # 计算结果
    result = numerator / denominator
    
    # 得到最简形式的分子与分母
    p, q = result.numerator, result.denominator
    
    # 返回 p + q
    return p + q

if __name__ == "__main__":
    print(unique_point_on_AB(1, 2, 3, 2))