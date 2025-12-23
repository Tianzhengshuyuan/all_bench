inputs = {'count_small': 2024}

from fractions import Fraction

def solve(count_small):
    R_small = 1
    M_small = count_small
    R_big = 34
    M_big = 8
    t = Fraction(2*R_small*(M_small - 1) - 2*R_big*(M_big - 1), R_big - R_small)
    BC_small = 2*R_small*(M_small - 1) + R_small * t
    r = BC_small / t
    return r.numerator + r.denominator

solve(2024)

# 调用 solve
result = solve(inputs['count_small'])
print(result)