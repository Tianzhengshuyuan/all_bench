inputs = {'volume': 23}

from fractions import Fraction
from math import acos, cos, pi

def solve(volume):
    # Maximize a^2+b^2+c^2 with ab+bc+ca=27 and abc=V.
    # By symmetry, at the extremum two edges are equal: let a=b=x, c=y.
    # Then x^2 + 2xy = 27 and x^2*y = V -> eliminate y: x^3 - 27x + 2V = 0.
    # For each positive real root x, y = V/x^2 and r^2 = (2x^2 + y^2)/4.
    V = Fraction(volume)
    if V <= 0 or V > 27:
        return None

    def r2_from_xy(x, y):
        return (2*x*x + y*y) / 4

    # Try exact rational roots first (Rational Root Theorem for x^3 - 27x + 2V = 0)
    def divisors(n):
        n = abs(n)
        ds = set()
        i = 1
        while i * i <= n:
            if n % i == 0:
                ds.add(i)
                ds.add(n // i)
            i += 1
        return ds

    exact_candidates = []
    twoV = 2 * V
    num, den = twoV.numerator, twoV.denominator
    if num != 0:
        Ps, Qs = divisors(abs(num)), divisors(den)
        seen = set()
        for p in Ps:
            for q in Qs:
                for s in (1, -1):
                    x = Fraction(s * p, q)
                    if x <= 0 or x in seen:
                        continue
                    seen.add(x)
                    if x**3 - 27*x + 2*V == 0:
                        y = V / (x*x)
                        if y > 0:
                            exact_candidates.append(r2_from_xy(x, y))

    # Numeric roots via trigonometric form for depressed cubic
    V_float = float(V)
    arg = -V_float / 27.0
    if arg < -1.0:
        arg = -1.0
    if arg > 1.0:
        arg = 1.0
    theta = acos(arg)
    numeric_best = None
    for k in (0, 1, 2):
        x = 6.0 * cos((theta + 2 * pi * k) / 3.0)
        if x > 1e-15:
            y = V_float / (x*x)
            if y > 0:
                r2 = (2.0 * x * x + y * y) / 4.0
                if numeric_best is None or r2 > numeric_best:
                    numeric_best = r2

    # Decide the best r^2, preferring exact if it matches numeric within tolerance
    best_exact = max(exact_candidates) if exact_candidates else None
    if best_exact is not None:
        if numeric_best is None or float(best_exact) >= numeric_best - 1e-12:
            r2 = best_exact.limit_denominator()
            return r2.numerator + r2.denominator

    from fractions import Fraction as Fr
    r2_frac = Fr(numeric_best).limit_denominator(10**12)
    return r2_frac.numerator + r2_frac.denominator

solve(23)

# 调用 solve
result = solve(inputs['volume'])
print(result)