inputs = {'r': '192/5'}

from fractions import Fraction

def solve(r):
    def to_fraction(x):
        if isinstance(x, Fraction):
            return x
        try:
            return Fraction(x).limit_denominator()
        except Exception:
            return Fraction(str(x)).limit_denominator()

    rr = to_fraction(r)
    R = Fraction(34, 1)  # radius of large circles
    N = 8                # number of large circles

    denom = rr - R
    if denom == 0:
        return None  # degenerate case

    t = Fraction(1, 1) + (rr - 1) * R * (N - 1) / denom
    t = t.limit_denominator()
    return t.numerator if t.denominator == 1 else t

solve(192/5)

# 调用 solve
result = solve(inputs['r'])
print(result)