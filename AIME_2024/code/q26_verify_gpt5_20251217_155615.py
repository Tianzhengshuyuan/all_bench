inputs = {'BC_length': 8}

from fractions import Fraction
from math import isqrt
from decimal import Decimal, getcontext

def solve(BC_length):
    # Given: AB = 5, AC = 10; variable: BC = BC_length
    a = Fraction(BC_length, 1)  # BC
    b = Fraction(7, 1)         # AC
    c = Fraction(6, 1)          # AB

    # Law of Cosines for cos A and cos B
    cosA = (b*b + c*c - a*a) / (2*b*c)
    cosB = (a*a + c*c - b*b) / (2*a*c)

    # In triangle BDC (tangents from D at B and C), angles at B and C are both A
    # Hence BD = CD = L, and BC = 2 L cos A => CD = BC / (2 cos A)
    CD = a / (2 * cosA)

    # In triangle ADC, angle ACD = 180° - B, so cos(angle ACD) = -cos B
    # AD^2 = AC^2 + CD^2 - 2*AC*CD*cos(ACD) = AC^2 + CD^2 + 2*AC*CD*cosB
    AD2 = b*b + CD*CD + 2*b*CD*cosB

    # Rational square root helper
    def sqrt_fraction(fr):
        num, den = fr.numerator, fr.denominator
        sn, sd = isqrt(num), isqrt(den)
        if sn*sn == num and sd*sd == den:
            return Fraction(sn, sd)
        # Fallback to high-precision numeric sqrt (shouldn't be needed for this input)
        getcontext().prec = 80
        sdec = (Decimal(num) / Decimal(den)).sqrt()
        return Fraction(sdec).limit_denominator(10**9)

    AD = sqrt_fraction(AD2)

    # Power of a Point from D: DA * DP = DB^2 = DC^2
    DP = (CD*CD) / AD

    # AP = AD - DP
    AP = AD - DP
    if AP < 0:
        AP = -AP
    AP = AP.limit_denominator()

    # AP = m/n in lowest terms
    m, n = AP.numerator, AP.denominator
    return m + n

# 调用 solve
result = solve(inputs['BC_length'])
print(result)