inputs = {'den_rhs_y': 523}

def solve(den_rhs_y):
    from fractions import Fraction
    s1 = Fraction(1, 2)
    s2 = Fraction(1, 1) / Fraction(den_rhs_y)
    s3 = Fraction(1, 4)
    a = Fraction(-1, 2) * (s2 + s3)
    b = Fraction(-1, 2) * (s1 + s3)
    c = Fraction(-1, 2) * (s1 + s2)
    val = 4 * a + 3 * b + 2 * c
    val = -val if val < 0 else val
    return val.numerator + val.denominator

solve(3)

# 调用 solve
result = solve(inputs['den_rhs_y'])
print(result)