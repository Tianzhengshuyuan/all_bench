inputs = {'r': '192/5'}

from fractions import Fraction

def solve(r):
    R = r
    if not isinstance(R, Fraction):
        if isinstance(R, float):
            R = Fraction.from_float(R).limit_denominator()
        else:
            R = Fraction(R)
    R34 = Fraction(34, 1)
    N34 = 8
    t = Fraction(1, 1) + (R - 1) * R34 * (N34 - 1) / (R - R34)
    return t.numerator if t.denominator == 1 else t

solve(Fraction(192, 5))

# 调用 solve
result = solve(inputs['r'])
print(result)