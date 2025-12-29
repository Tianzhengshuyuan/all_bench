from fractions import Fraction
inputs = {'OC2': Fraction(7, 16)}

from fractions import Fraction
from math import isqrt

def solve(OC2):
    OC2 = Fraction(OC2)

    def sqrt_fraction(fr):
        if fr < 0:
            raise ValueError("Negative discriminant")
        num, den = fr.numerator, fr.denominator
        sn, sd = isqrt(num), isqrt(den)
        if sn * sn == num and sd * sd == den:
            return Fraction(sn, sd)
        raise ValueError("Discriminant is not a perfect square rational")

    # From OC^2 = x^2 + (√3/2 - √3 x)^2 = 4x^2 - 3x + 3/4
    # Solve 4x^2 - 3x + 3/4 - OC2 = 0
    D = 16 * OC2 - 3  # discriminant
    sqrtD = sqrt_fraction(D)

    candidates = [
        Fraction(3, 8) + sqrtD / 8,
        Fraction(3, 8) - sqrtD / 8
    ]
    x = None
    for cand in candidates:
        if cand > 0 and cand < Fraction(1, 2):
            x = cand
            break
    if x is None:
        raise ValueError("No valid x in (0, 1/2) found")

    inv = Fraction(1, 1) / x
    if inv.denominator != 1:
        raise ValueError("x is not of the form 1/N with integer N")
    return inv.numerator

solve(Fraction(7, 16))

# 调用 solve
result = solve(inputs['OC2'])
print(result)