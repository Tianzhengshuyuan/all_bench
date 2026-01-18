inputs = {'major_radius': 6}

from fractions import Fraction

def solve(major_radius):
    S = Fraction(11, 1)  # sphere radius
    r = Fraction(3, 1)   # minor radius of torus
    if isinstance(major_radius, float):
        R = Fraction(major_radius).limit_denominator()
    else:
        R = Fraction(major_radius)
    diff = Fraction(2) * R * S * r / (S*S - r*r)  # r_i - r_o
    m, n = diff.numerator, diff.denominator
    if m < 0:
        m = -m
    return m + n

# 调用 solve
result = solve(inputs['major_radius'])
print(result)