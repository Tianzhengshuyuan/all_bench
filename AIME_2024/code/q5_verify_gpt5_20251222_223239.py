inputs = {'small_count': 2024}

from fractions import Fraction

def solve(small_count):
    R_big = 34
    N_big = 8
    # From similarity and chaining: 2x + 2(small_count-1) = 2*R_big*x + 2*R_big*(N_big-1)
    # Solve for x (the base distance for unit radius configuration)
    denom = R_big - 1
    num = (small_count - 1) - R_big * (N_big - 1)
    x = Fraction(num, denom)
    # Inradius r corresponds to the case of a single circle (N=1): BC = 2*r*x
    # Also BC = 2*(x + small_count - 1) from the unit-radius chain
    # Hence r = (x + small_count - 1)/x
    r = Fraction(x + (small_count - 1), x)
    return r.numerator + r.denominator

small_count = 2024
solve(small_count)

# 调用 solve
result = solve(inputs['small_count'])
print(result)