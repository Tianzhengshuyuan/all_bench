inputs = {'denominator': 3}

from fractions import Fraction

def solve(denominator):
    # Define logs: a = log2(x), b = log2(y), c = log2(z)
    # From the system:
    # a - b - c = 1/2
    # b - a - c = 1/denominator
    # c - a - b = 1/4
    # Adding equations pairwise yields:
    # -2a = 1/denominator + 1/4
    # -2b = 1/2 + 1/4
    # -2c = 1/2 + 1/denominator
    a = - (Fraction(1, denominator) + Fraction(1, 4)) * Fraction(1, 2)
    b = - (Fraction(1, 2) + Fraction(1, 4)) * Fraction(1, 2)
    c = - (Fraction(1, 2) + Fraction(1, denominator)) * Fraction(1, 2)
    
    val = abs(4*a + 3*b + 2*c)  # = |log2(x^4 y^3 z^2)|
    return val.numerator + val.denominator

# 调用 solve
result = solve(inputs['denominator'])
print(result)