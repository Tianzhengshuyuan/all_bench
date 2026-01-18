inputs = {'tan2': 3}

from fractions import Fraction

def solve(tan2):
    t = Fraction(tan2)
    oc2 = Fraction(1) - (t * t) / (1 + t) ** 2
    return oc2.numerator + oc2.denominator

tan2 = 3
solve(tan2)

# 调用 solve
result = solve(inputs['tan2'])
print(result)