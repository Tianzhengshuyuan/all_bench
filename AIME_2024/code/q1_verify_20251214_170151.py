inputs = {'exponent_y': 3}

from fractions import Fraction

def solve(exponent_y):
    # Given system:
    # a - b - c = 1/2
    # -a + b - c = 1/3
    # -a - b + c = 1/4
    r1 = Fraction(1, 2)
    r2 = Fraction(1, 3)
    r3 = Fraction(1, 4)

    # Solve for a = log2(x), b = log2(y), c = log2(z)
    c = -(r1 + r2) / 2
    b = -(r1 + r3) / 2
    a = -(r2 + r3) / 2

    # Compute |log2(x^4 * y^{exponent_y} * z^2)| = |4a + exponent_y*b + 2c|
    value = abs(4 * a + Fraction(exponent_y, 1) * b + 2 * c)

    # Return m + n where value = m/n in lowest terms
    return value.numerator + value.denominator

# 调用 solve
result = solve(inputs['exponent_y'])
print(result)