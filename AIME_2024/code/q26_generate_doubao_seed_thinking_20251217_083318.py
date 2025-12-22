inputs = {'AB_length': 6}

from fractions import Fraction
import math

def solve(AB_length):
    BC_length = 9
    AC_length = 10
    # Calculate cosA using Law of Cosines
    cos_A = Fraction(AB_length**2 + AC_length**2 - BC_length**2, 2 * AB_length * AC_length)
    # Calculate cosB using Law of Cosines
    cos_B = Fraction(AB_length**2 + BC_length**2 - AC_length**2, 2 * AB_length * BC_length)
    # Calculate CD: BC/2 divided by cosA
    BC_half = Fraction(BC_length, 2)
    CD = BC_half / cos_A
    # Calculate AD squared
    AC_squared = AC_length ** 2
    CD_squared = CD ** 2
    term3 = 2 * AC_length * CD * cos_B
    AD_squared = AC_squared + CD_squared + term3
    # Get AD by taking square root of AD_squared (which is a perfect square)
    AD_num = math.isqrt(AD_squared.numerator)
    AD_den = math.isqrt(AD_squared.denominator)
    AD = Fraction(AD_num, AD_den)
    # Calculate DP using Power of a Point: DP * AD = CD^2
    DP = CD_squared / AD
    # Calculate AP = AD - DP
    AP = AD - DP
    # Return m + n where AP = m/n in lowest terms
    return AP.numerator + AP.denominator

# 调用 solve
result = solve(inputs['AB_length'])
print(result)