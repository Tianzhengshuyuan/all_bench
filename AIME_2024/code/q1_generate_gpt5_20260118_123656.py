inputs = {'exp_x': 3}

def solve(exp_x):
    from fractions import Fraction
    r1 = Fraction(1, 2)
    r2 = Fraction(1, 3)
    r3 = Fraction(1, 4)
    a = -(r2 + r3) / 2
    b = -(r1 + r3) / 2
    c = -(r1 + r2) / 2
    ex = Fraction(exp_x, 1)
    val = abs(ex * a + 3 * b + 2 * c)
    return val.numerator + val.denominator

solve(4)

# 调用 solve
result = solve(inputs['exp_x'])
print(result)