inputs = {'denominator': 4}

from fractions import Fraction

def solve(denominator):
    r1 = Fraction(1, 2)
    r2 = Fraction(1, 3)
    r3 = Fraction(1, denominator)
    a = -(r2 + r3) / 2
    b = -(r1 + r3) / 2
    c = -(r1 + r2) / 2
    S = abs(4*a + 3*b + 2*c)
    return S.numerator + S.denominator

# 调用 solve
result = solve(inputs['denominator'])
print(result)