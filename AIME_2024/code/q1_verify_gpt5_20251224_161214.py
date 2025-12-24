inputs = {'log_x4y3z2_denominator': 8}

from fractions import Fraction

def solve(log_x4y3z2_denominator):
    D = Fraction(log_x4y3z2_denominator, 1)
    # log2(x/(yz)) = 10/D - 3/4, so N = 1 / (10/D - 3/4) = 4D / (40 - 3D)
    denom = 40 - 3 * D
    if denom == 0:
        return None
    N = Fraction(4 * D, denom)
    return N.numerator if N.denominator == 1 else N

solve(8)

# 调用 solve
result = solve(inputs['log_x4y3z2_denominator'])
print(result)