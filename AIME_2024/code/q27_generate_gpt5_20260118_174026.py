inputs = {None: 19}

from fractions import Fraction

def solve(_=None):
    a = Fraction(3, 1)   # tube radius of torus
    R = Fraction(6, 1)   # distance from circle center to axis (major radius)
    Rs = Fraction(11, 1) # sphere radius

    ri = Rs * R / (Rs - a)
    ro = Rs * R / (Rs + a)
    diff = ri - ro  # equals 2*a*R*Rs / (Rs^2 - a^2)

    return diff.numerator + diff.denominator

# 调用 solve
result = solve(inputs)
print(result)