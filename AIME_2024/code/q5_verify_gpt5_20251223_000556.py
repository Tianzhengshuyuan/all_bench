inputs = {'count': 2024}

from fractions import Fraction

def solve(count):
    R = 34
    n_big = 8
    s = Fraction(2 * ((count - 1) - R * (n_big - 1)), R - 1)
    BC = Fraction(2 * (count - 1)) + s
    r = BC / s
    return r.numerator + r.denominator

solve(2024)

# 调用 solve
result = solve(inputs['count'])
print(result)