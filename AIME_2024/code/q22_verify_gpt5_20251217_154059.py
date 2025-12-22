inputs = {'triangle_side_length': 240}

from fractions import Fraction

def solve(triangle_side_length):
    # Side lengths of the big triangle formed by extensions of AB, CD, EF
    # Given in the problem: 200, triangle_side_length (variable), 300
    a = 200
    b = triangle_side_length
    c = 300

    # From similarity, the hexagon side length x satisfies:
    # x = (a*b*c) / (ab + bc + ca)
    num = a * b * c
    den = a * b + b * c + c * a

    frac = Fraction(num, den)
    return frac.numerator if frac.denominator == 1 else float(frac)

# 调用 solve
result = solve(inputs['triangle_side_length'])
print(result)