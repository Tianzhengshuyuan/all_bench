inputs = {'generator_radius': 4}

from fractions import Fraction

def solve(generator_radius):
    ring_radius = 6
    sphere_radius = 11
    ri = Fraction(ring_radius * sphere_radius, sphere_radius - generator_radius)
    ro = Fraction(ring_radius * sphere_radius, sphere_radius + generator_radius)
    diff = ri - ro
    return diff.numerator + diff.denominator

# 调用 solve
result = solve(inputs['generator_radius'])
print(result)