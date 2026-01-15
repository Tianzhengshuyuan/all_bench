inputs = {'tube_radius': 1}

from fractions import Fraction

def solve(tube_radius):
    R = 11
    d = 6
    a = Fraction(tube_radius, 1)
    ri = Fraction(R * d, 1) / (R - a)
    ro = Fraction(R * d, 1) / (R + a)
    diff = ri - ro
    return diff.numerator + diff.denominator

solve(3)

# 调用 solve
result = solve(inputs['tube_radius'])
print(result)