inputs = {'r': '192/5'}

from fractions import Fraction

def solve(r):
    def to_fraction(x):
        if isinstance(x, Fraction):
            return x
        try:
            return Fraction(x).limit_denominator()
        except TypeError:
            return Fraction(str(x))

    rr = to_fraction(r)
    R = Fraction(34, 1)   # radius of large circles
    N = 8                 # number of large circles

    denom = rr - R
    if denom == 0:
        return None

    t = 1 + (rr - 1) * R * (N - 1) / denom

    if isinstance(t, Fraction) and t.denominator == 1:
        return t.numerator
    return float(t)

solve(192/5)

# 调用 solve
result = solve(inputs['r'])
print(result)