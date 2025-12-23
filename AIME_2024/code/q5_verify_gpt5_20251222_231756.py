inputs = {'count_small': 2024}

from fractions import Fraction

def solve(count_small):
    R_big = 34
    N_big = 8
    A = count_small - 1
    B = N_big - 1
    den = A - R_big * B
    r = Fraction(R_big * (A - B), den)
    return r.numerator + r.denominator

count_small = 2024
solve(count_small)

# 调用 solve
result = solve(inputs['count_small'])
print(result)