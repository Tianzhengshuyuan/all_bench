inputs = {'denominator': 3}

from fractions import Fraction

def solve(denominator):
    # Let a=log2(x), b=log2(y), c=log2(z)
    # From the system:
    # a - b - c = 1/2
    # -a + b - c = 1/denominator
    # -a - b + c = 1/4
    # Summing pairs gives:
    a = - (Fraction(1, denominator) + Fraction(1, 4)) / 2
    b = - (Fraction(1, 2) + Fraction(1, 4)) / 2
    c = - (Fraction(1, 2) + Fraction(1, denominator)) / 2

    value = abs(4*a + 3*b + 2*c)
    return value.numerator + value.denominator

# 调用 solve
result = solve(inputs['denominator'])
print(result)