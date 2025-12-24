inputs = {'log_x4y3z2_denominator': 8}

from fractions import Fraction

def solve(log_x4y3z2_denominator):
    den = Fraction(log_x4y3z2_denominator, 1)
    # From the two given equations:
    # b - a - c = 1/3 and c - a - b = 1/4
    # Derive a and (b - c)
    a = - (Fraction(1, 3) + Fraction(1, 4)) / 2  # a = -7/24
    bc_diff = (Fraction(1, 3) - Fraction(1, 4)) / 2  # b - c = 1/24

    # From -log2(x^4 y^3 z^2) = 25/den => 4a + 3b + 2c = -25/den
    rhs = -Fraction(25, 1) / den

    # Solve for c using 3b + 2c = rhs - 4a and b = c + bc_diff
    c = (rhs - 4 * a - 3 * bc_diff) / 5

    # Desired value: log2(x/(yz)) = a - b - c = a - (c + bc_diff) - c
    S = a - (c + bc_diff) - c

    # S = 1/N => N = 1/S
    N = Fraction(1, 1) / S
    return N.numerator if N.denominator == 1 else N

solve(8)

# 调用 solve
result = solve(inputs['log_x4y3z2_denominator'])
print(result)