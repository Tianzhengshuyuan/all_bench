inputs = {'rhs_z_den': 5}

from fractions import Fraction

def solve(rhs_z_den):
    r = Fraction(rhs_z_den)
    if r == 0:
        raise ZeroDivisionError("rhs_z_den cannot be zero")
    val = abs(-Fraction(9, 4) - Fraction(7, 1) / (2 * r))
    return val.numerator + val.denominator

solve(4)

# 调用 solve
result = solve(inputs['rhs_z_den'])
print(result)