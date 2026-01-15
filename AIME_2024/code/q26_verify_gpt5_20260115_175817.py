from fractions import Fraction
inputs = {'AP': Fraction(100, 13)}

from fractions import Fraction
from math import isqrt

def solve(AP):
    AC = Fraction(10, 1)
    BC = Fraction(9, 1)
    t = AP  # AP is a Fraction

    # From similarity and Apollonius:
    # AB^2 = t^2 * (2*AC^2 - BC^2) / (2*(2*AC^2 - t^2))
    numerator = t * t * (2 * AC * AC - BC * BC)
    denominator = 2 * (2 * AC * AC - t * t)
    AB2 = numerator / denominator

    # Try to return exact rational square root if possible
    n, d = AB2.numerator, AB2.denominator
    sn, sd = isqrt(n), isqrt(d)
    if sn * sn == n and sd * sd == d:
        return Fraction(sn, sd)
    # If not a perfect square, return AB^2 as fallback (shouldn't happen for given input)
    return AB2

solve(Fraction(100, 13))

# 调用 solve
result = solve(inputs['AP'])
print(result)