inputs = {'log_x4y3z2_denominator': 8}

from fractions import Fraction

def solve(log_x4y3z2_denominator):
    D = Fraction(log_x4y3z2_denominator, 1)
    if D == 0:
        return None
    s2 = Fraction(1, 3)
    s3 = Fraction(1, 4)
    s1 = (Fraction(50, 1) / D - 6 * s2 - 7 * s3) / 5
    if s1 == 0:
        return None
    N = Fraction(1, 1) / s1
    return N.numerator if N.denominator == 1 else N

log_x4y3z2_denominator = 8
solve(log_x4y3z2_denominator)

# 调用 solve
result = solve(inputs['log_x4y3z2_denominator'])
print(result)