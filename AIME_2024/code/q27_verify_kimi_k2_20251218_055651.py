inputs = {'torus_minor_radius': 3}

import math

def solve(torus_minor_radius):
    # Given: torus_minor_radius = 3
    # Distance from center of generating circle to axis = 6
    # Sphere radius = 11
    
    # For internal tangent:
    # Using similar triangles: (6 / (11 - torus_minor_radius)) = (r_i / 11)
    r_i = (6 * 11) / (11 - torus_minor_radius)
    
    # For external tangent:
    # Using similar triangles: (6 / (11 + torus_minor_radius)) = (r_o / 11)
    r_o = (6 * 11) / (11 + torus_minor_radius)
    
    # Difference
    diff = r_i - r_o
    
    # Convert to fraction
    from fractions import Fraction
    frac = Fraction(diff).limit_denominator()
    m, n = frac.numerator, frac.denominator
    
    return m + n

# 调用 solve
result = solve(inputs['torus_minor_radius'])
print(result)