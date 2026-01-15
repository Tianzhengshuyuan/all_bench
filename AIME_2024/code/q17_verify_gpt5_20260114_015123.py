inputs = {'volume': 23}

from fractions import Fraction
from math import acos, cos, pi

def solve(volume):
    # We need max of a^2+b^2+c^2 with ab+bc+ca=27 and abc=V.
    # By symmetry (Lagrange multipliers), at the extremum two edges are equal: let a=b=x, c=y.
    # Then: x^2 + 2xy = 27 and x^2 y = V -> eliminate y to get cubic: x^3 - 27x + 2V = 0.
    # For each positive real root x, y = V/x^2 and r^2 = (a^2+b^2+c^2)/4 = (2x^2 + y^2)/4.
    V = Fraction(volume)
    if V <= 0 or V > 27:
        return None

    def r2_from_xy(x, y):
        return (2*x*x + y*y) / 4

    candidates_exact = []

    # Try to find rational roots exactly (Rational Root Theorem)
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

    def F_frac(x):
        return x**3 - 27*x + 2*V

    twoV = 2 * V
    num, den = twoV.numerator, twoV.denominator
    if num != 0:
        Ps, Qs = divisors(abs(num)), divisors(den)
        seen = set()
        for p in Ps:
            for q in Qs:
                for s in (1, -1):
                    x = Fraction(s*p, q)
                    if x in seen or x <= 0:
                        continue
                    seen.add(x)
                    if F_frac(x) == 0:
                        y = V / (x*x)
                        if y > 0:
                            candidates_exact.append(r2_from_xy(x, y))

    # Numeric roots via trigonometric form for depressed cubic x^3 + px + q = 0
    # Here p = -27, q = 2V with 0 < V <= 27 so three real roots; take the positive ones.
    V_float = float(V)
    arg = -V_float / 27.0
    if arg < -1.0:
        arg = -1.0
    if arg > 1.0:
        arg = 1.0
    phi = acos(arg)
    numeric_r2_best = None
    for k in (0, 1, 2):
        x = 6.0 * cos((phi + 2 * pi * k) / 3.0)
        if x > 0:
            y = V_float / (x*x)
            if y > 0:
                r2 = (2.0 * x * x + y * y) / 4.0
                if numeric_r2_best is None or r2 > numeric_r2_best:
                    numeric_r2_best = r2

    # Choose the best r^2, preferring exact if it matches the numeric max within tolerance
    tol = 1e-12
    if candidates_exact:
        best_exact = max(candidates_exact)
        if numeric_r2_best is None or float(best_exact) >= numeric_r2_best - tol:
            best_exact = best_exact.limit_denominator()
            return best_exact.numerator + best_exact.denominator

    # Fallback to numeric best converted to a rational approximation
    r2_frac = Fraction(numeric_r2_best).limit_denominator(10**12)
    return r2_frac.numerator + r2_frac.denominator

volume = 23
solve(volume)

# 调用 solve
result = solve(inputs['volume'])
print(result)