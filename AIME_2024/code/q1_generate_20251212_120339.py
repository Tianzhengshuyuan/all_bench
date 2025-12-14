inputs = {'y_exponent': 3}

from fractions import Fraction

def solve(y_exponent):
    # Right-hand sides of the given system
    r1, r2, r3 = Fraction(1, 2), Fraction(1, 3), Fraction(1, 4)
    # Solve for a = log2(x), b = log2(y), c = log2(z)
    a = -(r2 + r3) / 2
    b = -(r1 + r3) / 2
    c = -(r1 + r2) / 2
    # Compute |log2(x^4 * y^{y_exponent} * z^2)|
    val = abs(4 * a + Fraction(y_exponent) * b + 2 * c)
    # Return m + n where val = m/n in lowest terms
    return val.numerator + val.denominator

# 调用 solve
result = solve(inputs['y_exponent'])
print(result)