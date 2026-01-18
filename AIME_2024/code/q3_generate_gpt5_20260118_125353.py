inputs = {'set_size': 16}

from math import comb
from fractions import Fraction

def solve(set_size):
    def nCk(n, k):
        if n < 0 or k < 0 or k > n:
            return 0
        return comb(n, k)
    numerator = nCk(4, 4) * nCk(set_size - 4, 0)
    denominator = sum(nCk(4, k) * nCk(set_size - 4, 4 - k) for k in (2, 3, 4))
    if denominator == 0:
        return 0
    frac = Fraction(numerator, denominator)
    return frac.numerator + frac.denominator

solve(10)

# 调用 solve
result = solve(inputs['set_size'])
print(result)