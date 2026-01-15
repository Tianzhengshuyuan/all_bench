from fractions import Fraction
inputs = {'neg_log_x4y3z2': Fraction(25, 8)}

from fractions import Fraction

def solve(neg_log_x4y3z2):
    q = Fraction(1, 3)  # log2(y/(xz))
    r = Fraction(1, 4)  # log2(z/(xy))
    # p = log2(x/(yz))
    p = Fraction(2, 5) * (neg_log_x4y3z2 - 3*q - Fraction(7, 2)*r)
    if p > 0 and p.numerator == 1:
        return p.denominator
    inv = Fraction(1, 1) / p if p != 0 else None
    if inv is not None and inv.denominator == 1 and inv > 0:
        return inv.numerator
    return p

solve(Fraction(25, 8))

# 调用 solve
result = solve(inputs['neg_log_x4y3z2'])
print(result)