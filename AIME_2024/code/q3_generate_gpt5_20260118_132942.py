inputs = {'pick_count': 9}

from math import comb
from fractions import Fraction

def solve(pick_count):
    S_size = 10
    draw = 4

    def C(n, k):
        if k < 0 or k > n:
            return 0
        return comb(n, k)

    k = pick_count
    denom = sum(C(k, r) * C(S_size - k, draw - r) for r in range(2, min(draw, k) + 1))
    num = C(k, draw)

    if denom == 0:
        return 0

    frac = Fraction(num, denom)
    return frac.numerator + frac.denominator

solve(4)

# 调用 solve
result = solve(inputs['pick_count'])
print(result)