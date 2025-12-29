from fractions import Fraction
inputs = {'r': Fraction(192, 5)}

from fractions import Fraction

def solve(r):
    R = Fraction(34, 1)
    r = Fraction(r)
    N_frac = Fraction(1, 1) + Fraction(7, 1) * R * (r - Fraction(1, 1)) / (r - R)
    return N_frac.numerator // N_frac.denominator if N_frac.denominator == 1 else N_frac

solve(Fraction(192, 5))

# 调用 solve
result = solve(inputs['r'])
print(result)