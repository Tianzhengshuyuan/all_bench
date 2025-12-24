inputs = {'log_x4y3z2_denominator': 8}

from fractions import Fraction

def solve(log_x4y3z2_denominator):
    D = Fraction(log_x4y3z2_denominator, 1)
    if D == 0:
        return None
    B = Fraction(1, 3)  # log2(y/(xz))
    C = Fraction(1, 4)  # log2(z/(xy))
    a = -(B + C) / 2
    delta = (B - C) / 2  # b - c
    # From 4a + 3b + 2c = -25/D, with 3b + 2c = (5/2)(b+c) + (1/2)(b-c)
    S = Fraction(2, 5) * (-Fraction(25, 1) / D - 4 * a - Fraction(1, 2) * delta)  # b + c
    A = a - S  # log2(x/(yz))
    if A == 0:
        return None
    N = Fraction(1, A)
    return N.numerator if N.denominator == 1 else N

solve(8)

# 调用 solve
result = solve(inputs['log_x4y3z2_denominator'])
print(result)