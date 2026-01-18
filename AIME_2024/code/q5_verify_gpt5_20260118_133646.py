inputs = {'small_count': 2024}

from fractions import Fraction

def solve(small_count):
    r_big = 34
    n_big = 8
    s = small_count
    delta = (s - 1) - (n_big - 1) * r_big
    rin = Fraction(1, 1) + Fraction((s - 1) * (r_big - 1), delta)
    return rin.numerator + rin.denominator

solve(small_count)

# 调用 solve
result = solve(inputs['small_count'])
print(result)