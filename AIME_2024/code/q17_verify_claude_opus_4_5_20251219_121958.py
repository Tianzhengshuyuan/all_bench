inputs = {'volume': 23}

from fractions import Fraction
import math
import numpy as np

def solve(volume):
    # Given: surface area = 54, volume = V
    # For a rectangular box with dimensions a, b, c:
    # Surface area: 2(ab + bc + ca) = 54, so ab + bc + ca = 27
    # Volume: abc = V
    # The smallest sphere containing the box has radius r = sqrt(a^2 + b^2 + c^2) / 2
    # We want to find the maximum of a^2 + b^2 + c^2 over all valid boxes
    
    S = 27  # half surface area (ab + bc + ca)
    V = volume  # abc
    
    # The hint says "height and width are the same in this antioptimal box"
    # So we look for the case where two dimensions are equal
    
    # Case 1: a = b
    # Then: a^2 + 2ac = S, a^2 * c = V
    # c = V/a^2, so a^2 + 2V/a = S
    # a^3 - Sa + 2V = 0
    
    # Case 2: b = c  
    # Then: ab + b^2 + ab = S => 2ab + b^2 = S, ab^2 = V
    # a = V/b^2, so 2V/b + b^2 = S
    # b^3 - Sb + 2V = 0 (same equation!)
    
    # Case 3: a = c
    # Then: ab + bc + a^2 = S => ab + ba + a^2 = S => 2ab + a^2 = S, a^2*b = V
    # b = V/a^2, so 2V/a + a^2 = S
    # a^3 - Sa + 2V = 0 (same equation!)
    
    # So all symmetric cases give: x^3 - Sx + 2V = 0
    # For S = 27, V = 23: x^3 - 27x + 46 = 0
    
    # Check if x = 2 is a root: 8 - 54 + 46 = 0 ✓
    # Factor: (x - 2)(x^2 + 2x - 23) = 0
    # Other roots: x = (-2 ± sqrt(4 + 92))/2 = -1 ± sqrt(24) = -1 ± 2*sqrt(6)
    
    sqrt6 = math.sqrt(6)
    
    # For a = b case with a = 2:
    a1 = 2
    c1 = V / (a1**2)
    sum_sq1 = 2 * a1**2 + c1**2
    
    # For a = b case with a = -1 + 2*sqrt(6):
    a2 = -1 + 2*sqrt6
    c2 = V / (a2**2)
    sum_sq2 = 2 * a2**2 + c2**2
    
    # For b = c case, we need: 2ab + b^2 = S, ab^2 = V
    # b^3 - Sb + 2V = 0 is WRONG for this case
    # Correct: b = c, so ab + b*b + b*a = S => 2ab + b^2 = S
    # And ab*b = V => ab^2 = V => a = V/b^2
    # Substituting: 2(V/b^2)*b + b^2 = S => 2V/b + b^2 = S
    # b^3 - Sb + 2V = 0
    
    # Wait, let me reconsider. For b = c:
    # ab + bc + ca = ab + b^2 + ab = 2ab + b^2 = S
    # abc = ab^2 = V
    # So a = V/b^2, and 2V/b + b^2 = S
    # b^3 + 2V = Sb => b^3 - Sb + 2V = 0
    
    # This is the same cubic! So for b = c with b = 2:
    b1 = 2
    a1_bc = V / (b1**2)
    sum_sq1_bc = a1_bc**2 + 2*b1**2
    
    # For b = c with b = -1 + 2*sqrt(6):
    b2 = -1 + 2*sqrt6
    a2_bc = V / (b2**2)
    sum_sq2_bc = a2_bc**2 + 2*b2**2
    
    # Now find the maximum
    all_sum_sq = [sum_sq1, sum_sq2, sum_sq1_bc, sum_sq2_bc]
    max_sum_sq = max(all_sum_sq)
    
    # Let's compute exact values
    # For a = b = 2, c = V/4:
    # sum_sq = 2*4 + V^2/16 = 8 + V^2/16 = (128 + V^2)/16
    
    # For b = c = 2, a = V/4:
    # sum_sq = (V/4)^2 + 2*4 = V^2/16 + 8 = (V^2 + 128)/16
    # Same!
    
    # For a = b = -1 + 2*sqrt(6), c = V/(25 - 4*sqrt(6)):
    # a^2 = 1 - 4*sqrt(6) + 24 = 25 - 4*sqrt(6)
    # sum_sq = 2*(25 - 4*sqrt(6)) + V^2/(25 - 4*sqrt(6))^2
    
    # For b = c = -1 + 2*sqrt(6), a = V/(25 - 4*sqrt(6)):
    # sum_sq = V^2/(25 - 4*sqrt(6))^2 + 2*(25 - 4*sqrt(6))
    # Same!
    
    # Compare numerically:
    # sum_sq1 = 8 + 529/16 = 657/16 ≈ 41.0625
    # sum_sq2 ≈ 2*(25 - 9.798) + 529/(25-9.798)^2 ≈ 30.4 + 2.29 ≈ 32.7
    
    # So the maximum is at a = b = 2, c = V/4 (or equivalently b = c = 2, a = V/4)
    
    # r^2 = sum_sq / 4 = (128 + V^2) / 64
    
    # For V = 23: r^2 = (128 + 529) / 64 = 657/64
    
    # But wait - let me verify the constraint for a = b = 2, c = 23/4:
    # ab + bc + ca = 4 + 2*(23/4) + 2*(23/4) = 4 + 23 = 27 ✓
    # abc = 4 * 23/4 = 23 ✓
    
    # And for b = c = 2, a = 23/4:
    # ab + bc + ca = (23/4)*2 + 4 + (23/4)*2 = 23 + 4 = 27 ✓
    # abc = (23/4)*4 = 23 ✓
    
    # Both give sum_sq = (23/4)^2 + 8 = 529/16 + 128/16 = 657/16
    # r^2 = 657/64
    
    # gcd(657, 64): 657 = 9*73, 64 = 2^6, gcd = 1
    
    numerator = 128 + V**2
    denominator = 64
    
    from math import gcd
    g = gcd(numerator, denominator)
    p = numerator // g
    q = denominator // g
    
    return p + q

result = solve(23)

# 调用 solve
result = solve(inputs['volume'])
print(result)