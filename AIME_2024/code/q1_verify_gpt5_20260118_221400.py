from fractions import Fraction
inputs = {'neg_log2_x4y3z2': Fraction(25, 8)}

from fractions import Fraction

def solve(neg_log2_x4y3z2):
    S = Fraction(neg_log2_x4y3z2)
    # T = log2(x/(yz)) = (2*S - 6*(1/3) - 7*(1/4)) / 5 = (2/5)S - 3/4
    T = Fraction(2, 5) * S - Fraction(3, 4)
    N = Fraction(1, 1) / T
    return N.numerator if N.denominator == 1 else N

# 调用 solve
result = solve(inputs['neg_log2_x4y3z2'])
print(result)