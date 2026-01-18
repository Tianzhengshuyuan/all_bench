inputs = {'exp_y': 3}

from fractions import Fraction

def solve(exp_y):
    r1, r2, r3 = Fraction(1, 2), Fraction(1, 3), Fraction(1, 4)
    a = -(r2 + r3) / 2
    b = -(r1 + r3) / 2
    c = -(r1 + r2) / 2
    ey = Fraction(exp_y)
    val = abs(4 * a + ey * b + 2 * c)
    return val.numerator + val.denominator

solve(3)

# 调用 solve
result = solve(inputs['exp_y'])
print(result)