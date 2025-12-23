inputs = {'sphere_radius': 293}

from fractions import Fraction

def solve(sphere_radius):
    s = Fraction(sphere_radius)
    a = Fraction(3, 1)  # tube radius of torus
    R = Fraction(6, 1)  # distance from circle center to axis
    # r_i - r_o = 2*a*R*s / (s^2 - a^2)
    diff = 2 * a * R * s / (s * s - a * a)
    frac = Fraction(diff)
    num = abs(frac.numerator)
    den = frac.denominator
    return num + den

solve(11)

# 调用 solve
result = solve(inputs['sphere_radius'])
print(result)