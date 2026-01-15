inputs = {'BC': 13}

from fractions import Fraction
import math

def solve(BC):
    # AB = 5, AC = 10
    # AP = 100 / sqrt(250 - BC^2)
    s = Fraction(250) - Fraction(BC)**2  # s = 250 - BC^2

    def is_square(n):
        if n < 0:
            return False
        r = math.isqrt(n)
        return r * r == n

    a, b = s.numerator, s.denominator
    if is_square(a) and is_square(b):
        sqrt_s = Fraction(math.isqrt(a), math.isqrt(b))
        ap = Fraction(100) / sqrt_s  # AP as a reduced Fraction
        m, n = ap.numerator, ap.denominator
        if n < 0:
            m, n = -m, -n
        return m + n
    else:
        return None

solve(9)

# 调用 solve
result = solve(inputs['BC'])
print(result)