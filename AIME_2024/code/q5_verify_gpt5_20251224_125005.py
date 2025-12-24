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

    R2 = 34
    n = 8
    rr = to_fraction(r)
    R = Fraction(R2, 1)

    if rr == R:
        return None  # degenerate case

    x = R * (n - 1) / (rr - R)
    t = 1 + (rr - 1) * x

    if isinstance(t, Fraction) and t.denominator == 1:
        return t.numerator
    return float(t)

solve(192/5)

# 调用 solve
result = solve(inputs['r'])
print(result)