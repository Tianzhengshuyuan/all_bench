inputs = {'rhs_z_den': 993}

from fractions import Fraction

def solve(rhs_z_den):
    s1 = Fraction(1, 2)
    s2 = Fraction(1, 3)
    den = Fraction(rhs_z_den)
    s3 = Fraction(1, 1) / den
    a = - (s2 + s3) / 2
    b = - (s1 + s3) / 2
    c = - (s1 + s2) / 2
    val = abs(4*a + 3*b + 2*c)
    return val.numerator + val.denominator

rhs_z_den = 4
solve(rhs_z_den)

# 调用 solve
result = solve(inputs['rhs_z_den'])
print(result)