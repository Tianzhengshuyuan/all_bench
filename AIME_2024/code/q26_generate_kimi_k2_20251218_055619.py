inputs = {'AC_length': 798}

import math
from fractions import Fraction

def solve(AC_length):
    # Given side lengths
    AB = 5
    BC = 9
    AC = AC_length
    
    # Compute cos A using Law of Cosines
    cos_A = (AB**2 + AC**2 - BC**2) / (2 * AB * AC)
    
    # Compute cos B using Law of Cosines
    cos_B = (AB**2 + BC**2 - AC**2) / (2 * AB * BC)
    
    # Compute CD: CD = (BC/2) / cos_A
    CD = (BC / 2) / cos_A
    
    # Compute angle A + B
    # cos(A+B) = cos A cos B - sin A sin B
    sin_A = math.sqrt(1 - cos_A**2)
    sin_B = math.sqrt(1 - cos_B**2)
    cos_A_plus_B = cos_A * cos_B - sin_A * sin_B
    
    # But we need cos(A + C) = cos(180 - B) = -cos B
    cos_A_plus_C = -cos_B
    
    # Compute AD^2 using Law of Cosines in triangle ACD
    AD_squared = AC**2 + CD**2 - 2 * AC * CD * cos_A_plus_C
    AD = math.sqrt(AD_squared)
    
    # Power of a Point: DP * AD = CD^2
    DP = CD**2 / AD
    
    AP = AD - DP
    
    # Convert to fraction
    AP_frac = Fraction(AP).limit_denominator()
    m, n = AP_frac.numerator, AP_frac.denominator
    return m + n

# Example usage:
# print(solve(10))

# 调用 solve
result = solve(inputs['AC_length'])
print(result)