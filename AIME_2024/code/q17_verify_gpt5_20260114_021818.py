inputs = {'volume': 23}

from fractions import Fraction
from math import acos, cos, pi

def solve(volume):
    V = Fraction(volume)

    # Feasible range for positive edges with ab+bc+ca=27 is 0 < V <= 27
    if V <= 0 or V > 27:
        return None

    def r2_from_x(x):
        y = V / (x * x)
        if y <= 0:
            return None
        return (2 * x * x + y * y) / 4

    # Try exact rational roots for b*x^3 - 27*b*x + 2*a = 0 where V = a/b
    a, b = V.numerator, V.denominator

    def divisors(n):
        n = abs(n)
        ds = set()
        i = 1
        while i * i <= n:
            if n % i == 0:
                ds.add(i)
                ds.add(n // i)
            i += 1
        return ds if ds else {1}

    roots_exact = []
    if a != 0:
        Ps, Qs = divisors(2 * a), divisors(b if b != 0 else 1)
        seen = set()
        for p in Ps:
            for q in Qs:
                for s in (1, -1):
                    x = Fraction(s * p, q)
                    if x <= 0 or x in seen:
                        continue
                    seen.add(x)
                    if b * x**3 - 27 * b * x + 2 * a == 0:
                        roots_exact.append(x)

    exact_candidates = []
    for x in roots_exact:
        r2 = r2_from_x(x)
        if r2 is not None:
            exact_candidates.append(r2)

    # Numeric roots via trigonometric form for depressed cubic x^3 - 27x + 2V = 0
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
            y = V_float / (x * x)
            if y > 0:
                r2 = (2.0 * x * x + y * y) / 4.0
                if numeric_best is None or r2 > numeric_best:
                    numeric_best = r2

    # Prefer exact result if it matches numeric within tolerance
    if exact_candidates:
        best_exact = max(exact_candidates)
        if numeric_best is None or abs(float(best_exact) - numeric_best) <= 1e-12 * max(1.0, numeric_best):
            r2 = best_exact.limit_denominator()
            return r2.numerator + r2.denominator

    r2_frac = Fraction(numeric_best).limit_denominator(10**12)
    return r2_frac.numerator + r2_frac.denominator

volume = 23
solve(volume)

# 调用 solve
result = solve(inputs['volume'])
print(result)