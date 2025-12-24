inputs = {'log_x4y3z2_denominator': 8}

from fractions import Fraction

def solve(log_x4y3z2_denominator):
    d = Fraction(log_x4y3z2_denominator, 1)
    s2 = Fraction(1, 3)  # log2(y/(xz))
    s3 = Fraction(1, 4)  # log2(z/(xy))
    # From 4a + 3b + 2c = -25/d and 4a+3b+2c = -(5/2)s1 - 3*s2 - (7/2)*s3
    # => -5*s1 - 6*s2 - 7*s3 = -50/d
    # => s1 = (50/d - 6*s2 - 7*s3)/5
    s1 = (Fraction(50, d) - 6*s2 - 7*s3) / 5  # s1 = log2(x/(yz))
    N = Fraction(1, s1)
    return N.numerator if N.denominator == 1 else N

log_x4y3z2_denominator = 8
solve(log_x4y3z2_denominator)

# 调用 solve
result = solve(inputs['log_x4y3z2_denominator'])
print(result)