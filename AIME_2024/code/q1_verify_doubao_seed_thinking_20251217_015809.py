inputs = {'exponent_x': 4}

from fractions import Fraction

def solve(exponent_x):
    a = Fraction(-7, 24)
    b = Fraction(-3, 8)
    c = Fraction(-5, 12)
    value = exponent_x * a + 3 * b + 2 * c
    abs_fraction = abs(value)
    return abs_fraction.numerator + abs_fraction.denominator

# 调用 solve
result = solve(inputs['exponent_x'])
print(result)