from fractions import Fraction
inputs = {'r': Fraction(192, 5)}

from fractions import Fraction

def solve(r):
    r = Fraction(r)
    R_big = Fraction(34, 1)
    n_big = 8
    x = R_big * Fraction(n_big - 1, 1) / (r - R_big)
    N = Fraction(1, 1) + (r - Fraction(1, 1)) * x
    return N

solve(Fraction(192, 5))

# 调用 solve
result = solve(inputs['r'])
print(result)