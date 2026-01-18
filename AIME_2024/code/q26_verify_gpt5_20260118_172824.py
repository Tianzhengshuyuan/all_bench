inputs = {'AB': 5}

from fractions import Fraction
from math import isqrt, sqrt

def solve(AB):
    # Helper: exact sqrt of a Fraction if it is a perfect square, else return None
    def sqrt_fraction(fr):
        n, d = fr.numerator, fr.denominator
        sn, sd = isqrt(n), isqrt(d)
        if sn * sn == n and sd * sd == d:
            return Fraction(sn, sd)
        return None

    # Given fixed sides from the problem
    a = Fraction(9, 1)   # BC
    b = Fraction(10, 1)  # AC
    c = Fraction(AB)     # AB (variable)

    # Compute DC using angle-chasing: DC = (BC/2)/cos A,
    # with cos A from Law of Cosines; simplified to DC = (a*b*c)/(b^2 + c^2 - a^2)
    Dden = b*b + c*c - a*a
    DC = (a * b * c) / Dden

    # Compute AD^2 via Law of Cosines in triangle ACD:
    # AD^2 = b^2 + DC^2 + 2*b*DC*cos B,
    # with cos B = (a^2 + c^2 - b^2)/(2ac) so that 2*b*DC*cos B = b^2*(a^2 + c^2 - b^2)/Dden
    AD2 = b*b + DC*DC + b*b * (a*a + c*c - b*b) / Dden

    # Try exact sqrt
    AD = sqrt_fraction(AD2)
    if AD is None:
        # Fallback to float if not a perfect square (not expected for the given test)
        AD_float = sqrt(float(AD2))
        AP_float = AD_float - float(DC*DC) / AD_float
        ap_frac = Fraction(AP_float).limit_denominator(10**9)
        return ap_frac.numerator + ap_frac.denominator

    # Power of a Point from D: DC^2 = DA * DP, and along D-P-A we have AP = AD - DP = AD - DC^2/AD
    AP = AD - (DC*DC) / AD  # exact Fraction when AD is Fraction

    # Return m + n for AP = m/n in lowest terms
    AP = AP.limit_denominator()  # ensure reduced
    return AP.numerator + AP.denominator

# 调用 solve
result = solve(inputs['AB'])
print(result)