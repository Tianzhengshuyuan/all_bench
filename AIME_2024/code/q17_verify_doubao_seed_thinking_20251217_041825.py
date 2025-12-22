inputs = {'volume': 23}

import numpy as np
from fractions import Fraction

def solve(volume):
    V = volume
    coeff = [1, 0, -27, 2 * V]
    roots = np.roots(coeff)
    real_pos_roots = []
    for r in roots:
        if abs(r.imag) < 1e-9:
            real_r = r.real
            if real_r > 1e-9:
                real_pos_roots.append(real_r)
    max_s = 0.0
    for t in real_pos_roots:
        a = V / (t ** 2)
        s = a ** 2 + 2 * (t ** 2)
        if s > max_s:
            max_s = s
    r_squared = max_s / 4
    frac = Fraction(r_squared).limit_denominator()
    return frac.numerator + frac.denominator

# 调用 solve
result = solve(inputs['volume'])
print(result)