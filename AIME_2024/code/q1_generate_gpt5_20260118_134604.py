inputs = {'exp_y': 2}

from fractions import Fraction

def solve(exp_y):
    # Right-hand sides of the logarithmic system
    r1 = Fraction(1, 2)  # log2(x/(yz))
    r2 = Fraction(1, 3)  # log2(y/(xz))
    r3 = Fraction(1, 4)  # log2(z/(xy))

    # Let A = log2(x), B = log2(y), C = log2(z)
    # From adding pairs of equations:
    # -2C = r1 + r2, -2B = r1 + r3, -2A = r2 + r3
    A = - (r2 + r3) * Fraction(1, 2)
    B = - (r1 + r3) * Fraction(1, 2)
    C = - (r1 + r2) * Fraction(1, 2)

    k = Fraction(exp_y)
    val = abs(4*A + k*B + 2*C)  # |log2(x^4 y^k z^2)|

    return val.numerator + val.denominator

# 调用 solve
result = solve(inputs['exp_y'])
print(result)