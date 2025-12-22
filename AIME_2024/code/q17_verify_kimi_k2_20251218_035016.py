inputs = {'surface_area': 54}

import numpy as np
from scipy.optimize import minimize
import fractions

def solve(surface_area):
    # Given surface_area = 54 and volume = 23
    V = 23
    S = surface_area
    
    # The radius of the smallest sphere that can contain a rectangular box with dimensions a, b, c
    # is half of the space diagonal: r = sqrt(a^2 + b^2 + c^2) / 2
    # So r^2 = (a^2 + b^2 + c^2) / 4
    
    # We want to minimize r^2 subject to:
    # 1) abc = V
    # 2) 2(ab + bc + ca) = S
    
    # Let x = a^2, y = b^2, z = c^2
    # Then r^2 = (x + y + z)/4
    # We want to minimize x + y + z
    
    # From abc = V => a^2 b^2 c^2 = V^2 => xyz = V^2
    # From 2(ab + bc + ca) = S => ab + bc + ca = S/2
    
    # Let u = ab, v = bc, w = ca
    # Then u + v + w = S/2
    # And uvw = (ab)(bc)(ca) = a^2 b^2 c^2 = V^2
    
    # Also, u/v = a/c, v/w = b/a, w/u = c/b
    # So u/v * v/w * w/u = 1 => (a/c)(b/a)(c/b) = 1 ✓
    
    # We can express a, b, c in terms of u, v, w:
    # a = sqrt(uw/v), b = sqrt(uv/w), c = sqrt(vw/u)
    
    # Then a^2 + b^2 + c^2 = uw/v + uv/w + vw/u
    
    # We want to minimize uw/v + uv/w + vw/u subject to u + v + w = S/2 and uvw = V^2
    
    # By symmetry and the hint that "the height and the width are the same in this antioptimal box",
    # we can assume b = c (i.e., the box has a square cross-section)
    
    # Let b = c => y = z
    # Then from abc = V => a b^2 = V => a = V / b^2
    # From surface area: 2(ab + bc + ca) = 2(a b + b^2 + a b) = 2(2ab + b^2) = 4ab + 2b^2 = S
    # Substitute a = V / b^2: 4(V / b^2) b + 2b^2 = 4V / b + 2b^2 = S
    # => 2b^2 + 4V / b = S
    # => 2b^3 - S b + 4V = 0
    
    # Solve cubic equation: 2b^3 - S b + 4V = 0
    coeffs = [2, 0, -S, 4*V]
    roots = np.roots(coeffs)
    real_positive_roots = [r.real for r in roots if abs(r.imag) < 1e-10 and r.real > 0]
    
    if not real_positive_roots:
        return None  # No valid solution
    
    b = real_positive_roots[0]
    a = V / (b**2)
    c = b  # since b = c
    
    # Calculate r^2
    r_squared = (a**2 + b**2 + c**2) / 4
    
    # Convert to fraction
    frac = fractions.Fraction(r_squared).limit_denominator()
    p, q = frac.numerator, frac.denominator
    
    return p + q

# Test with the given surface area
print(solve(54))

# 调用 solve
result = solve(inputs['surface_area'])
print(result)