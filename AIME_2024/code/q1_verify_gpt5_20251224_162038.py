inputs = {'log_x4y3z2_denominator': 8}

from fractions import Fraction

def solve(log_x4y3z2_denominator):
    D = Fraction(log_x4y3z2_denominator, 1)
    if D == 0:
        return None
    # Let a = log2(x), b = log2(y), c = log2(z)
    # Given:
    # b - a - c = 1/3
    # c - a - b = 1/4
    # 4a + 3b + 2c = -25/D
    B = Fraction(1, 3)
    C = Fraction(1, 4)
    a = -(B + C) / 2
    d = (B - C) / 2  # b - c
    rhs = -Fraction(25, 1) / D
    c = (rhs - 4 * a - 3 * d) / 5
    A = a - (c + d) - c  # log2(x/(yz))
    if A == 0:
        return None
    N = Fraction(1, 1) / A
    return N.numerator if N.denominator == 1 else N

solve(8)

# 调用 solve
result = solve(inputs['log_x4y3z2_denominator'])
print(result)