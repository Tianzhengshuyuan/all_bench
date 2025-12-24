inputs = {'inradius': 192}

from fractions import Fraction

def solve(inradius):
    R = 34
    N = 8
    r = Fraction(inradius, 5)
    numerator = 2*R*(N - 1) * (r - 1)
    denominator = 2*r - 2*R
    if denominator == 0:
        return None
    n = 1 + numerator / denominator
    return n.numerator if isinstance(n, Fraction) and n.denominator == 1 else n

solve(192)

# 调用 solve
result = solve(inputs['inradius'])
print(result)