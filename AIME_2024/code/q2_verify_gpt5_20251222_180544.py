inputs = {'radicand': 3}

from fractions import Fraction

def solve(radicand):
    x = Fraction(1, 8)
    oc2 = x*x + Fraction(radicand) * (Fraction(1, 2) - x) ** 2
    return oc2.numerator + oc2.denominator

solve(3)

# 调用 solve
result = solve(inputs['radicand'])
print(result)