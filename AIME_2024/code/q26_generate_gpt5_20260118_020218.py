inputs = {'AB_length': 11}

from fractions import Fraction
from math import isqrt, sqrt

def solve(AB_length):
    # Given constants from the problem
    a = 9   # BC
    b = 10  # AC
    c = AB_length  # AB (variable)
    
    def sqrt_fraction(frac):
        frac = Fraction(frac)
        if frac < 0:
            return None
        N = frac.numerator
        D = frac.denominator
        sN = isqrt(N)
        sD = isqrt(D)
        if sN * sN == N and sD * sD == D:
            return Fraction(sN, sD)
        return None

    # Apollonius: AM^2 = (2(b^2 + c^2) - a^2)/4
    m2 = Fraction(2*(b*b + c*c) - a*a, 4)
    AM = sqrt_fraction(m2)
    if AM is not None and AM != 0:
        AP = Fraction(b*c, 1) / AM
        AP = AP if AP >= 0 else -AP
        AP = AP.limit_denominator()
        return AP.numerator + AP.denominator

    # Fallback for non-rational AM: approximate and rationalize
    AM_float = sqrt(float(m2))
    AP_float = (b*c) / AM_float
    AP_frac = Fraction(AP_float).limit_denominator(10**9)
    return AP_frac.numerator + AP_frac.denominator

solve(5)

# 调用 solve
result = solve(inputs['AB_length'])
print(result)