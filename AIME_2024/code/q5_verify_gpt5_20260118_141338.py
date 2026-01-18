inputs = {'small_count': 2024}

from fractions import Fraction

def solve(small_count):
    R = 34
    N = 8
    n = small_count
    denom = (n - 1) - R * (N - 1)
    r = Fraction(1, 1) + Fraction((n - 1) * (R - 1), denom)
    return r.numerator + r.denominator

# 调用 solve
result = solve(inputs['small_count'])
print(result)