inputs = {'sphere_radius': 11}

from fractions import Fraction

def solve(sphere_radius):
    a = 3      # minor (tube) radius of the torus
    R = 6      # major radius (distance from axis to tube center)
    S = sphere_radius  # sphere radius
    diff = Fraction(2 * a * R * S, S * S - a * a)  # r_i - r_o simplified
    return diff.numerator + diff.denominator

# 调用 solve
result = solve(inputs['sphere_radius'])
print(result)