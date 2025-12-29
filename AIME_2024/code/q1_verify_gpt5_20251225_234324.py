from fractions import Fraction
inputs = {'neg_log2_x4y3z2': Fraction(25, 8)}

from fractions import Fraction

def solve(neg_log2_x4y3z2):
    T = Fraction(2, 5) * neg_log2_x4y3z2 - Fraction(3, 4)
    return Fraction(1, T)

solve(Fraction(25, 8))

# 调用 solve
result = solve(inputs['neg_log2_x4y3z2'])
print(result)