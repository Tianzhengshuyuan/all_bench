inputs = {'x_exponent': 4}

from fractions import Fraction

def solve(x_exponent):
    half = Fraction(1, 2)
    third = Fraction(1, 3)
    quarter = Fraction(1, 4)
    a = - (third + quarter) / 2  # log2 x
    b = - (half + quarter) / 2   # log2 y
    c = - (half + third) / 2     # log2 z
    val = abs(Fraction(x_exponent) * a + 3 * b + 2 * c)
    return val.numerator + val.denominator

solve(4)

# 调用 solve
result = solve(inputs['x_exponent'])
print(result)