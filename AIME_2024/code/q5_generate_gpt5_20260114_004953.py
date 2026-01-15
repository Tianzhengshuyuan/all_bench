inputs = {'count': 422}

from fractions import Fraction

def solve(count):
    R_big = 34
    N_big = 8
    x = Fraction(count - (R_big * (N_big - 1) + 1), R_big - 1)
    r = Fraction(1, 1) + Fraction(count - 1, 1) / x
    return r.numerator + r.denominator

solve(2024)

# 调用 solve
result = solve(inputs['count'])
print(result)