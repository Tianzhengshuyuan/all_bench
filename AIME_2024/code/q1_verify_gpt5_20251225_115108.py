from fractions import Fraction
inputs = {'neg_log_x4y3z2': Fraction(25, 8)}

from fractions import Fraction

def solve(neg_log_x4y3z2):
    Nneg = Fraction(neg_log_x4y3z2)
    a = - (Fraction(1, 3) + Fraction(1, 4)) / 2
    D = a + Fraction(1, 3)  # b - c
    S = (-2 * Nneg - 8 * a - D) / 5  # b + c
    L = a - S  # log2(x/(yz))
    N = Fraction(1, L)
    return N.numerator if N.denominator == 1 else N

solve(Fraction(25, 8))

# 调用 solve
result = solve(inputs['neg_log_x4y3z2'])
print(result)