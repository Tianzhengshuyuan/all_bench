inputs = {'rhs1': 0.5}

from fractions import Fraction

def solve(rhs1):
    r1 = Fraction(rhs1).limit_denominator()
    r2 = Fraction(1, 3)
    r3 = Fraction(1, 4)
    S_abs = abs((Fraction(5, 2) * r1) + (3 * r2) + (Fraction(7, 2) * r3))
    return S_abs.numerator + S_abs.denominator

solve(rhs1)

# 调用 solve
result = solve(inputs['rhs1'])
print(result)