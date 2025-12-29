from fractions import Fraction
inputs = {'neg_log_x4y3z2': Fraction(25, 8)}

from fractions import Fraction

def solve(neg_log_x4y3z2):
    T = Fraction(neg_log_x4y3z2)
    # Let a = log2(x), b = log2(y), c = log2(z)
    # From given: b - a - c = 1/3, c - a - b = 1/4, and 4a + 3b + 2c = -T
    a = - (Fraction(1,3) + Fraction(1,4)) / 2  # a = -7/24
    d = a + Fraction(1,3)  # d = b - c = 1/24
    c = (-T - 4*a - 3*d) / 5
    b = c + d
    k = a - b - c  # k = log2(x/(yz)) = 1/N
    N = Fraction(1,1) / k
    return N.numerator if N.denominator == 1 else N

solve(Fraction(25, 8))

# 调用 solve
result = solve(inputs['neg_log_x4y3z2'])
print(result)