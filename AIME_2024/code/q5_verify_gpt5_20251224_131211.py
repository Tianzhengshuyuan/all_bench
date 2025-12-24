inputs = {'r': '192/5'}

from fractions import Fraction

def solve(r):
    r = Fraction(r).limit_denominator()
    R2 = Fraction(34, 1)
    n2 = 8
    if r == R2:
        return None
    t = 1 + R2 * (n2 - 1) * (r - 1) / (r - R2)
    return t.numerator // t.denominator if t.denominator == 1 else t

solve(192/5)

# 调用 solve
result = solve(inputs['r'])
print(result)