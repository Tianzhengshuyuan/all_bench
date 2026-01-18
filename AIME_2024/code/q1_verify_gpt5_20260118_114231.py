inputs = {'exp_y': 3}

from fractions import Fraction

def solve(exp_y):
    r1 = Fraction(1, 2)
    r2 = Fraction(1, 3)
    r3 = Fraction(1, 4)

    c = -(r2 + r1) / 2
    b = -(r3 + r1) / 2
    a = r1 + b + c

    exp_y_frac = Fraction(exp_y).limit_denominator()
    value = abs(4 * a + exp_y_frac * b + 2 * c)

    m, n = value.numerator, value.denominator
    return m + n

solve(3)

# 调用 solve
result = solve(inputs['exp_y'])
print(result)