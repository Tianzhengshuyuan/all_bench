inputs = {'volume': 23}

from scipy.optimize import minimize_scalar, brentq
import numpy as np

def solve(volume):
    # Given: surface area = 54, volume = V
    # For a rectangular box with dimensions a, b, c:
    # Surface area: 2(ab + bc + ca) = 54, so ab + bc + ca = 27
    # Volume: abc = V
    # The smallest sphere containing the box has radius r = sqrt(a^2 + b^2 + c^2) / 2
    # We want to find the maximum of a^2 + b^2 + c^2 over all valid boxes
    
    S = 54  # surface area
    V = volume
    
    # ab + bc + ca = 27
    # abc = V
    # We want to maximize a^2 + b^2 + c^2
    
    # By symmetry, the maximum length box has two equal dimensions
    # Let's say b = c, then:
    # 2ab + b^2 = 27
    # ab^2 = V
    # From the second equation: a = V/b^2
    # Substituting: 2(V/b^2)b + b^2 = 27
    # 2V/b + b^2 = 27
    # b^3 - 27b + 2V = 0
    
    # We need to find b such that b^3 - 27b + 2V = 0
    # Then a = V/b^2
    # And r^2 = (a^2 + 2b^2) / 4
    
    def cubic(b):
        return b**3 - 27*b + 2*V
    
    # Find the roots of the cubic
    # The cubic b^3 - 27b + 2V = 0
    # Derivative: 3b^2 - 27 = 0 => b = ±3
    # Local max at b = -3, local min at b = 3
    # f(3) = 27 - 81 + 2V = 2V - 54 = 2*23 - 54 = -8 < 0
    # f(-3) = -27 + 81 + 2V = 54 + 2V > 0
    # So there's one root > 3, one root between -3 and 3, one root < -3
    
    # We need positive b, so we look for roots > 0
    # Since f(3) < 0 and f(∞) = ∞, there's a root > 3
    # Since f(0) = 2V > 0 and f(3) < 0, there's a root between 0 and 3
    
    # Find the root > 3 (this gives the longest box)
    b1 = brentq(cubic, 3, 100)
    a1 = V / (b1**2)
    r2_1 = (a1**2 + 2*b1**2) / 4
    
    # Find the root between 0 and 3
    b2 = brentq(cubic, 0.1, 3)
    a2 = V / (b2**2)
    r2_2 = (a2**2 + 2*b2**2) / 4
    
    # The maximum r^2 is the one we want
    r2_max = max(r2_1, r2_2)
    
    # Now we need to express r^2 as p/q in lowest terms
    # Let's compute it more precisely
    # For the case b = c, we have:
    # b^3 - 27b + 2V = 0
    # a = V/b^2
    # r^2 = (a^2 + 2b^2)/4 = (V^2/b^4 + 2b^2)/4
    
    # Let's verify which case gives maximum
    # For V = 23, the root > 3 should give the maximum
    
    # To get exact answer, we use the fact that for the optimal box:
    # b^3 - 27b + 46 = 0 (when V = 23)
    # We need to find r^2 = (V^2/b^4 + 2b^2)/4
    
    # From b^3 = 27b - 46, we have b^3 = 27b - 46
    # Let's compute r^2 in terms of b
    
    # Actually, let's use numerical approach to find p and q
    from fractions import Fraction
    
    # Use high precision
    b_opt = b1 if r2_1 > r2_2 else b2
    a_opt = V / (b_opt**2)
    
    # r^2 = (a^2 + b^2 + c^2) / 4 where c = b
    r2 = (a_opt**2 + 2*b_opt**2) / 4
    
    # Try to find the fraction
    frac = Fraction(r2).limit_denominator(10000)
    
    # Let's verify by computing exactly
    # For the maximum, we need to check if it's at b = c case
    # The answer should be p + q where r^2 = p/q
    
    # From the problem, we know the answer involves the "antioptimal" box
    # where height = width (b = c)
    
    # Let me recalculate more carefully
    # We want the SMALLEST sphere that can contain EACH box in B
    # This means we want the MAXIMUM of the circumradius over all boxes
    
    # The circumradius of a box with dimensions a, b, c is sqrt(a^2+b^2+c^2)/2
    # So r^2 = (a^2+b^2+c^2)/4
    
    # We need to maximize a^2+b^2+c^2 subject to:
    # ab+bc+ca = 27
    # abc = 23
    
    # Using Lagrange multipliers or substitution
    # At the maximum, by symmetry arguments, two dimensions are equal
    
    # For b = c: b^3 - 27b + 46 = 0
    # The largest root gives the longest a (smallest b)
    
    # Let's find the exact value
    # b^3 - 27b + 46 = 0
    # We can check: b = 1 gives 1 - 27 + 46 = 20 ≠ 0
    # b = 2 gives 8 - 54 + 46 = 0 ✓
    
    # So b = 2 is a root!
    # Factor: (b-2)(b^2 + 2b - 23) = 0
    # Other roots: b = (-2 ± sqrt(4+92))/2 = (-2 ± sqrt(96))/2 = -1 ± 2sqrt(6)
    
    # Positive roots: b = 2 and b = -1 + 2sqrt(6) ≈ 3.899
    
    # For b = 2: a = 23/4, r^2 = ((23/4)^2 + 2*4)/4 = (529/16 + 8)/4 = (529/16 + 128/16)/4 = 657/64
    # For b = -1 + 2sqrt(6): a = 23/(-1+2sqrt(6))^2 = 23/(1 - 4sqrt(6) + 24) = 23/(25 - 4sqrt(6))
    
    b_val = 2
    a_val = 23/4
    r2_case1 = (a_val**2 + 2*b_val**2) / 4
    # = ((23/4)^2 + 8) / 4 = (529/16 + 128/16) / 4 = 657/64
    
    b_val2 = -1 + 2*np.sqrt(6)
    a_val2 = 23 / (b_val2**2)
    r2_case2 = (a_val2**2 + 2*b_val2**2) / 4
    
    if r2_case1 > r2_case2:
        # r^2 = 657/64
        p, q = 657, 64
    else:
        # Need to compute the other case exactly
        # b = -1 + 2sqrt(6), b^2 = 1 - 4sqrt(6) + 24 = 25 - 4sqrt(6)
        # a = 23/(25 - 4sqrt(6)) = 23(25 + 4sqrt(6))/((25)^2 - 16*6) = 23(25+4sqrt(6))/(625-96) = 23(25+4sqrt(6))/529
        # a = (25 + 4sqrt(6))/23
        # a^2 = (625 + 200sqrt(6) + 96)/529 = (721 + 200sqrt(6))/529
        # 2b^2 = 2(25 - 4sqrt(6)) = 50 - 8sqrt(6)
        # a^2 + 2b^2 = (721 + 200sqrt(6))/529 + 50 - 8sqrt(6)
        # = (721 + 200sqrt(6) + 529*50 - 529*8sqrt(6))/529
        # = (721 + 26450 + (200 - 4232)sqrt(6))/529
        # = (27171 - 4032sqrt(6))/529
        # This has sqrt(6), so it's irrational - can't be p/q
        # So the maximum must be at b = 2
        p, q = 657, 64
    
    # Verify gcd(657, 64) = 1
    from math import gcd
    g = gcd(657, 64)
    p, q = p // g, q // g
    
    return p + q

result = solve(23)

# 调用 solve
result = solve(inputs['volume'])
print(result)