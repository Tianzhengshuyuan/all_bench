inputs = {'radius_large': 34}

from fractions import Fraction

def solve(radius_large):
    N_small = 2024
    N_large = 8
    A = 2 * N_small - 2
    B = 2 * N_large - 2
    R2 = Fraction(radius_large).limit_denominator()
    r = Fraction(1, 1) + Fraction(A) * (R2 - 1) / (Fraction(A) - R2 * Fraction(B))
    r = r.limit_denominator()
    return r.numerator + r.denominator

solve(34)

# 调用 solve
result = solve(inputs['radius_large'])
print(result)