inputs = {'x_exp': 10}

from fractions import Fraction

def solve(x_exp):
    r1 = Fraction(1, 2)
    r2 = Fraction(1, 3)
    r3 = Fraction(1, 4)
    a = -(r2 + r3) / 2
    b = -(r1 + r3) / 2
    c = -(r1 + r2) / 2
    x_exp = Fraction(x_exp, 1)
    val = abs(x_exp * a + 3 * b + 2 * c)
    return val.numerator + val.denominator

solve(4)

# 调用 solve
result = solve(inputs['x_exp'])
print(result)