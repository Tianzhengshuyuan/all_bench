inputs = {'exponent_y': 3}

from fractions import Fraction

def solve(exponent_y):
    r1 = Fraction(1, 2)
    r2 = Fraction(1, 3)
    r3 = Fraction(1, 4)
    c = -(r1 + r2) / 2
    b = -(r1 + r3) / 2
    a = -(r2 + r3) / 2
    k = Fraction(exponent_y)
    val = abs(4*a + k*b + 2*c)
    return val.numerator + val.denominator

solve(3)

# 调用 solve
result = solve(inputs['exponent_y'])
print(result)