inputs = {'r': '192/5'}

from fractions import Fraction

def solve(r):
    R = 34  # radius of large circles
    n_large = 8  # number of large circles
    rF = Fraction(r)
    t = 1 + Fraction(R * (n_large - 1)) * (rF - 1) / (rF - R)
    return t.numerator if t.denominator == 1 else t

solve(Fraction(192, 5))

# 调用 solve
result = solve(inputs['r'])
print(result)