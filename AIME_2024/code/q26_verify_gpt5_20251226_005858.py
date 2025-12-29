from fractions import Fraction
inputs = {'AP': Fraction(100, 13)}

from fractions import Fraction
import math

def sqrt_fraction(frac):
    if frac < 0:
        raise ValueError("Negative fraction cannot have real square root")
    n = frac.numerator
    d = frac.denominator
    sn = math.isqrt(n)
    sd = math.isqrt(d)
    if sn * sn == n and sd * sd == d:
        return Fraction(sn, sd)
    raise ValueError("Square root is not a rational number")

def solve(AP):
    AC = Fraction(10, 1)
    BC = Fraction(9, 1)
    AP = Fraction(AP)

    AC2 = AC * AC
    BC2 = BC * BC
    K = Fraction(2, 1) * AC2 - BC2  # 2*AC^2 - BC^2

    numerator = K * AP * AP
    denominator = Fraction(4, 1) * AC2 - Fraction(2, 1) * AP * AP
    AB2 = numerator / denominator
    AB = sqrt_fraction(AB2)
    return AB

solve(Fraction(100, 13))

# 调用 solve
result = solve(inputs['AP'])
print(result)