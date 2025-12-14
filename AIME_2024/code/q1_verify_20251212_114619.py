inputs = {'exponent_y': 3}

from fractions import Fraction

def solve(exponent_y):
    # Given system:
    # a - b - c = 1/2
    # -a + b - c = 1/3
    # -a - b + c = 1/4
    s1 = Fraction(1, 2)
    s2 = Fraction(1, 3)
    s3 = Fraction(1, 4)

    # Solve for a = log2(x), b = log2(y), c = log2(z)
    a = -(s2 + s3) / 2
    b = -(s1 + s3) / 2
    c = -(s1 + s2) / 2

    # Compute |4a + exponent_y*b + 2c|
    val = abs(4*a + Fraction(exponent_y, 1)*b + 2*c)

    # Return m + n where val = m/n in lowest terms
    return val.numerator + val.denominator

# 调用 solve
result = solve(inputs['exponent_y'])
print(result)