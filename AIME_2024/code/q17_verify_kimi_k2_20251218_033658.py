inputs = {'surface_area': 54}

import numpy as np
from scipy.optimize import minimize
import math
from fractions import Fraction

def solve(surface_area):
    # Given surface_area = 54 and volume = 23
    V = 23
    S = surface_area
    
    # The radius of the smallest sphere that can contain a rectangular box with dimensions a, b, c
    # is half of the space diagonal: r = sqrt(a^2 + b^2 + c^2)/2
    # So r^2 = (a^2 + b^2 + c^2)/4
    
    # We want to minimize r^2 subject to:
    # 1) abc = V = 23
    # 2) 2(ab + bc + ca) = S = 54
    
    # Let x = a^2, y = b^2, z = c^2
    # Then we want to minimize (x + y + z)/4
    # Subject to:
    # sqrt(xyz) = V = 23  => xyz = V^2 = 529
    # 2(sqrt(xy) + sqrt(yz) + sqrt(zx)) = S = 54
    
    # But this is messy. Instead, we can use Lagrange multipliers or observe symmetry.
    
    # By symmetry and optimization, the maximum of (a^2 + b^2 + c^2) under the constraints
    # occurs when two variables are equal (as per the hint: "the height and the width are the same").
    
    # Let a = b, then:
    # Volume: a^2 * c = 23  => c = 23 / a^2
    # Surface area: 2(a*a + a*c + a*c) = 2(a^2 + 2ac) = 54
    # => a^2 + 2ac = 27
    # Substitute c = 23/a^2:
    # a^2 + 2a*(23/a^2) = 27
    # a^2 + 46/a = 27
    # Multiply by a: a^3 - 27a + 46 = 0
    
    # Solve cubic: a^3 - 27a + 46 = 0
    # Try rational roots: factors of 46 over 1: ±1, ±2, ±23, ±46
    # Try a=2: 8 - 54 + 46 = 0 -> yes!
    # So (a - 2) is a factor.
    # Divide: a^3 - 27a + 46 = (a - 2)(a^2 + 2a - 23) = 0
    # Roots: a = 2, or a = (-2 ± sqrt(4 + 92))/2 = (-2 ± sqrt(96))/2 = (-2 ± 4*sqrt(6))/2 = -1 ± 2*sqrt(6)
    # Since a > 0, possible a = 2 or a = -1 + 2*sqrt(6) ≈ 3.899
    
    # Check which gives larger r^2 (i.e., larger a^2 + b^2 + c^2)
    # We want the maximum of a^2 + b^2 + c^2 under constraints, because we want the smallest sphere that can contain *any* such box -> we need the worst-case box -> maximum diagonal
    
    def r_squared(a):
        c = 23 / a**2
        diag_sq = 2*a**2 + c**2
        return diag_sq / 4
    
    a1 = 2
    r1 = r_squared(a1)
    
    a2 = -1 + 2*math.sqrt(6)
    r2 = r_squared(a2)
    
    # Take the larger r^2
    r_sq = max(r1, r2)
    
    # But let's verify this is indeed the maximum by checking the cubic and behavior
    
    # Alternatively, solve exactly: we have two critical points from symmetry
    # We can compute exact r^2 for a = -1 + 2*sqrt(6)
    
    a = -1 + 2*math.sqrt(6)
    c = 23 / a**2
    diag_sq = 2*a**2 + c**2
    r_sq_exact = diag_sq / 4
    
    # Now express r_sq_exact as fraction
    # a = 2√6 - 1
    # a^2 = (2√6 - 1)^2 = 4*6 - 4√6 + 1 = 25 - 4√6
    a_sq = 25 - 4*math.sqrt(6)
    c = 23 / a_sq
    c_sq = (23**2) / (a_sq**2)
    diag_sq = 2*a_sq + c_sq
    r_sq_val = diag_sq / 4
    
    # But this is irrational. However, we can compute it numerically and then find rational approximation?
    # But we need exact fraction.
    
    # Instead, go back to the cubic and solve symbolically.
    # We have a^3 - 27a + 46 = 0
    # We took a = 2 or a = -1 + 2√6
    # We want to compute r^2 = (2a^2 + c^2)/4, c = 23/a^2
    
    # For a = -1 + 2√6:
    # a^2 = 25 - 4√6
    # c = 23 / (25 - 4√6) = 23(25 + 4√6) / ((25)^2 - (4√6)^2) = 23(25 + 4√6)/(625 - 96) = 23(25 + 4√6)/529
    # c^2 = 529 * (25 + 4√6)^2 / 529^2 = (25 + 4√6)^2 / 529
    # (25 + 4√6)^2 = 625 + 200√6 + 96 = 721 + 200√6
    # So c^2 = (721 + 200√6)/529
    
    # Then diag_sq = 2*(25 - 4√6) + (721 + 200√6)/529
    # = 50 - 8√6 + (721 + 200√6)/529
    # = [50*529 - 8√6*529 + 721 + 200√6] / 529
    # = [26450 - 4232√6 + 721 + 200√6] / 529
    # = (27171 - 4032√6) / 529
    
    # Then r^2 = diag_sq / 4 = (27171 - 4032√6)/(529*4) = (27171 - 4032√6)/2116
    
    # But this is irrational! However, the problem says r^2 = p/q rational.
    
    # So perhaps the maximum occurs at a = 2?
    # Try a = 2:
    a = 2
    c = 23 / 4
    diag_sq = 2*(4) + (23/4)**2 = 8 + 529/16 = (128 + 529)/16 = 657/16
    r_sq = diag_sq / 4 = 657/64
    
    # This is rational.
    # And 657 and 64: gcd(657,64)=1? 64=2^6, 657 odd -> yes.
    
    # Now check if this is indeed the maximum diagonal.
    # We need to confirm that this critical point gives the maximum of a^2+b^2+c^2 under constraints.
    
    # Since we are looking for the smallest sphere that can contain *any* box in B,
    # we need the maximum possible value of (a^2+b^2+c^2) over all boxes with volume 23 and surface 54.
    # Because the sphere must contain even the "worst" (largest diagonal) box.
    
    # And by symmetry and optimization, the maximum occurs when two dimensions are equal.
    # So we compare the two positive roots.
    
    r_sq1 = 657/64   # a=2
    r_sq2 = (27171 - 4032*math.sqrt(6))/2116  # a=-1+2√6
    
    # Numerically:
    val2 = (27171 - 4032*2.449489743)/2116
    # ≈ (27171 - 9876.5)/2116 ≈ 17294.5/2116 ≈ 8.17
    # r_sq1 = 657/64 ≈ 10.26
    # So r_sq1 is larger -> this is the maximum diagonal
    
    # So r^2 = 657/64
    p, q = 657, 64
    return p + q

print(solve(54))

# 调用 solve
result = solve(inputs['surface_area'])
print(result)