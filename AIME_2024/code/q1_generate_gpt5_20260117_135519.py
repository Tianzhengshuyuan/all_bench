inputs = {'rhs_den_z': 3}

from fractions import Fraction

def solve(rhs_den_z):
    rhs = Fraction(rhs_den_z)
    value = abs((Fraction(9) * rhs + Fraction(14)) / (Fraction(4) * rhs))
    return value.numerator + value.denominator

solve(4)

# 调用 solve
result = solve(inputs['rhs_den_z'])
print(result)