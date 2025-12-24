inputs = {'log_x4y3z2_denominator': 8}

from fractions import Fraction

def solve(log_x4y3z2_denominator):
    D = Fraction(log_x4y3z2_denominator, 1)
    if D == 0:
        return None
    # A = log2(x/(yz)) = 10/D - 3/4
    A = Fraction(10, 1) / D - Fraction(3, 4)
    if A == 0:
        return None
    N = Fraction(1, 1) / A
    return N.numerator if N.denominator == 1 else N

log_x4y3z2_denominator = 8
solve(log_x4y3z2_denominator)

# 调用 solve
result = solve(inputs['log_x4y3z2_denominator'])
print(result)