from fractions import Fraction
inputs = {'AP': Fraction(100, 13)}

from fractions import Fraction
from math import isqrt

def solve(AP):
    # Given triangle with fixed sides: BC = 9, AC = 10
    a = Fraction(9, 1)   # BC
    b = Fraction(10, 1)  # AC

    # From similarity (symmedian): AP * AM = b * c, where c = AB
    # With Apollonius: AM^2 = (c^2 + b^2)/2 - (a^2)/4
    # Let x = c^2, then:
    # AP^2 * ((x + b^2)/2 - a^2/4) = b^2 * x
    # Solve for x:
    A2 = AP * AP
    numerator = A2 * (a*a - 2*b*b)
    denominator = 2 * (A2 - 2*b*b)
    if denominator == 0:
        raise ZeroDivisionError("Invalid AP leading to division by zero.")
    x = numerator / denominator  # x = c^2

    if x < 0:
        raise ValueError("Computed AB^2 is negative, invalid configuration for given AP.")

    # Compute sqrt of Fraction exactly
    num = x.numerator
    den = x.denominator
    s_num = isqrt(num)
    s_den = isqrt(den)
    if s_num * s_num != num or s_den * s_den != den:
        raise ValueError("AB is not a rational number for the given AP.")
    AB = Fraction(s_num, s_den)
    return AB

solve(Fraction(100, 13))

# 调用 solve
result = solve(inputs['AP'])
print(result)