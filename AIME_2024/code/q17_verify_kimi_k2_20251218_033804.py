inputs = {'surface_area': 54}

import math
from fractions import Fraction

def solve(surface_area):
    # Given surface_area = 54, volume = 23
    # ab + bc + ca = 27, abc = 23
    # maximize a^2 + b^2 + c^2 = (a+b+c)^2 - 54
    # maximum of a+b+c occurs when two variables equal (b=c)
    # b^3 - 27b + 46 = 0  =>  (b-2)(b^2 + 2b - 23) = 0
    # positive roots: b = 2, b = -1 + 2√6
    candidates = []
    for b in [2.0, -1 + 2*math.sqrt(6)]:
        if b <= 0:
            continue
        a = (27 - b*b) / (2*b)
        if a <= 0:
            continue
        c = b
        if abs(a*b*c - 23) > 1e-12:
            continue
        s = a + b + c
        candidates.append(s)
    max_sum = max(candidates)
    diag_sq = max_sum**2 - 54
    r_squared = diag_sq / 4
    frac = Fraction(r_squared).limit_denominator(1000000)
    return frac.numerator + frac.denominator

# 调用 solve
result = solve(inputs['surface_area'])
print(result)