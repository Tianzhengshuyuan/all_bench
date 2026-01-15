inputs = {'count': 2024}

from fractions import Fraction

def solve(count):
    R_big = 34
    N_big = 8
    # Solve for x using BC equality for small (radius 1, count circles) and big (radius 34, 8 circles)
    # x = (count - (R_big*(N_big-1) + 1)) / (R_big - 1)
    x = Fraction(count - (R_big * (N_big - 1) + 1), R_big - 1)
    r = Fraction(1, 1) + Fraction(count - 1, 1) / x
    return r.numerator + r.denominator

solve(count)

# 调用 solve
result = solve(inputs['count'])
print(result)