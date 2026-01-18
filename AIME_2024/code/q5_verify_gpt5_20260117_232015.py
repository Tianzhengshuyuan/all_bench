inputs = {'small_count': 2024}

from fractions import Fraction

def solve(small_count):
    R = 34
    M = 8
    N = small_count
    x = Fraction((N - 1) - R * (M - 1), R - 1)
    r = Fraction(1, 1) + Fraction(N - 1, 1) / x
    return r.numerator + r.denominator

solve(small_count)

# 调用 solve
result = solve(inputs['small_count'])
print(result)