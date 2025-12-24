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
    R = Fraction(34, 1)
    N = 8

    if rr == R:
        return None  # degenerate case: denominator zero

    t = 1 + (rr - 1) * R * (N - 1) / (rr - R)

    if isinstance(t, Fraction) and t.denominator == 1:
        return t.numerator
    return t

solve(192/5)

# 调用 solve
result = solve(inputs['r'])
print(result)