from fractions import Fraction
inputs = {'ri_minus_ro': Fraction(99, 28)}

from fractions import Fraction
from math import isqrt

def solve(ri_minus_ro):
    def sqrt_fraction(fr):
        n, d = fr.numerator, fr.denominator
        sn, sd = isqrt(n), isqrt(d)
        if sn * sn == n and sd * sd == d:
            return Fraction(sn, sd)
        raise ValueError("The value under the square root is not a perfect square rational.")
    
    k = ri_minus_ro if isinstance(ri_minus_ro, Fraction) else Fraction(ri_minus_ro)
    if k == 0:
        return Fraction(0, 1)
    
    a = Fraction(3, 1)
    c = Fraction(6, 1)
    
    sqrt_term = sqrt_fraction(c * c + k * k)
    R = a * (c + sqrt_term) / k
    return R

solve(Fraction(99, 28))

# 调用 solve
result = solve(inputs['ri_minus_ro'])
print(result)