inputs = {'abac': 468}

from fractions import Fraction

def solve(abac):
    R = 13
    r = Fraction(abac, 6 * R)
    return r.numerator if r.denominator == 1 else float(r)

solve(468)

# 调用 solve
result = solve(inputs['abac'])
print(result)