inputs = {'rhs1_denom': 2}

from fractions import Fraction

def solve(rhs1_denom):
    d1 = Fraction(1, 1) / Fraction(rhs1_denom)
    d2 = Fraction(1, 3)
    d3 = Fraction(1, 4)
    a = -(d2 + d3) / 2
    b = -(d1 + d3) / 2
    c = -(d1 + d2) / 2
    val = abs(4*a + 3*b + 2*c)
    return val.numerator + val.denominator

solve(rhs1_denom)

# 调用 solve
result = solve(inputs['rhs1_denom'])
print(result)