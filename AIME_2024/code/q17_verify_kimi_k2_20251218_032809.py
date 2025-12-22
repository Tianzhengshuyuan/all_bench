inputs = {'surface_area': 54}

import math
from fractions import Fraction

def solve(surface_area):
    # Given surface_area = 54, volume = 23
    # Let dimensions be a, b, c
    # 2(ab + bc + ca) = surface_area
    # abc = 23
    # We want to minimize the circumradius of the box, which is half the space diagonal:
    # r = sqrt(a^2 + b^2 + c^2)/2
    # So we want to minimize a^2 + b^2 + c^2
    
    # From abc = 23, we can express c = 23/(ab)
    # Substitute into surface area equation:
    # 2(ab + b*(23/(ab)) + a*(23/(ab))) = 54
    # 2(ab + 23/a + 23/b) = 54
    # ab + 23/a + 23/b = 27
    # Multiply by ab:
    # a^2 b^2 + 23b + 23a = 27ab
    # a^2 b^2 - 27ab + 23a + 23b = 0
    
    # We can use symmetry: the maximum of a^2 + b^2 + c^2 under constraints occurs when two variables are equal
    # Let a = b, then c = 23/a^2
    # Surface area: 2(a^2 + 2*a*(23/a^2)) = 54
    # 2(a^2 + 46/a) = 54
    # a^2 + 46/a = 27
    # a^3 - 27a + 46 = 0
    # Try rational roots: possible roots are factors of 46
    # Try a = 2: 8 - 54 + 46 = 0 → works!
    # So a = 2 is a root
    # Factor: (a - 2)(a^2 + 2a - 23) = 0
    # Other roots: a = (-2 ± sqrt(4 + 92))/2 = (-2 ± sqrt(96))/2 = (-2 ± 4*sqrt(6))/2 = -1 ± 2*sqrt(6)
    # Take positive root: a = -1 + 2*sqrt(6)
    
    # Check which gives larger diagonal:
    # Case 1: a = b = 2, c = 23/4 = 5.75
    a1, b1, c1 = 2, 2, 23/4
    diag1 = a1**2 + b1**2 + c1**2
    
    # Case 2: a = b = -1 + 2*sqrt(6), c = 23/a^2
    a2 = -1 + 2*math.sqrt(6)
    b2 = a2
    c2 = 23 / (a2**2)
    diag2 = a2**2 + b2**2 + c2**2
    
    # The maximum diagonal gives the maximum r^2
    max_diag = max(diag1, diag2)
    r_squared = max_diag / 4
    
    # Convert to fraction
    frac = Fraction(r_squared).limit_denominator()
    p, q = frac.numerator, frac.denominator
    return p + q

# Example usage:
# print(solve(54))

# 调用 solve
result = solve(inputs['surface_area'])
print(result)