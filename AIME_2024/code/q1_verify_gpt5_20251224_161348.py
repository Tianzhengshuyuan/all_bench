inputs = {'log_x4y3z2_denominator': 8}

from fractions import Fraction

def solve(log_x4y3z2_denominator):
    D = Fraction(log_x4y3z2_denominator, 1)
    B = Fraction(1, 3)
    C = Fraction(1, 4)
    T = Fraction(25, 1) / D  # -log2(x^4 y^3 z^2) = 25/D
    A = Fraction(2, 5) * (T - 3 * B - Fraction(7, 2) * C)  # log2(x/(yz))
    if A == 0:
        return None
    N = Fraction(1, A)
    return N.numerator if N.denominator == 1 else N

solve(8)

# 调用 solve
result = solve(inputs['log_x4y3z2_denominator'])
print(result)