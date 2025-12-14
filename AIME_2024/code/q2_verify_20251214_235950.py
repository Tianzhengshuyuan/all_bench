inputs = {'radicand': 3}

from fractions import Fraction

def solve(radicand):
    r = Fraction(radicand, 1)
    d = Fraction(-3, 2 * (1 + r))
    x = Fraction(1, 2) + d
    oc2 = x * x + r * (Fraction(1, 2) - x) ** 2
    oc2 = oc2.limit_denominator()
    return oc2.numerator + oc2.denominator

# 调用 solve
result = solve(inputs['radicand'])
print(result)