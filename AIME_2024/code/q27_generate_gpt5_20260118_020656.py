inputs = {'sphere_radius': 10}

from fractions import Fraction

def solve(sphere_radius):
    tube_radius = 3
    major_radius = 6
    s = sphere_radius
    diff = Fraction(2 * s * major_radius * tube_radius, s * s - tube_radius * tube_radius)
    diff = abs(diff)
    return diff.numerator + diff.denominator

solve(11)

# 调用 solve
result = solve(inputs['sphere_radius'])
print(result)