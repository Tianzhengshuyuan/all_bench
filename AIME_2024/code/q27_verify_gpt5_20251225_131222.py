from fractions import Fraction
inputs = {'ri_minus_ro': Fraction(99, 28)}

from fractions import Fraction
from math import isqrt

def solve(ri_minus_ro):
    D = Fraction(ri_minus_ro)
    if D == 0:
        return None
    p, q = D.numerator, D.denominator
    s2 = 36 * q * q + p * p
    s = isqrt(s2)
    R = Fraction(18 * q + 3 * s, p)
    return R.numerator if R.denominator == 1 else R

solve(Fraction(99, 28))

# 调用 solve
result = solve(inputs['ri_minus_ro'])
print(result)