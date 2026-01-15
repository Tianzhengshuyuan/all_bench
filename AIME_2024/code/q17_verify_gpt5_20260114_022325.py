inputs = {'volume': 23}

from fractions import Fraction
from math import acos, cos, pi

def solve(volume):
    V = Fraction(volume)

    # Feasible set exists only for 0 < V <= 27 (max at a=b=c=3)
    if V <= 0 or V > 27:
        return None

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

    def r2_exact_from_x(x):
        # Using s1 = a+b+c = (3x^2+27)/(2x), r^2 = (s1^2 - 54)/4
        s1 = (3 * x * x + 27) / (2 * x)
        return (s1 * s1 - 54) / 4

    # Try exact rational roots for cubic: b*x^3 - 27*b*x + 2*a = 0 where V = a/b
    a, b = V.numerator, V.denominator
    exact_candidates = []
    if a != 0:
        Ps, Qs = divisors(2 * a), divisors(b if b != 0 else 1)
        seen = set()
        for p in Ps:
            for q in Qs:
                for sgn in (1, -1):
                    x = Fraction(sgn * p, q)
                    if x <= 0 or x in seen:
                        continue
                    seen.add(x)
                    if b * x**3 - 27 * b * x + 2 * a == 0:
                        exact_candidates.append(r2_exact_from_x(x))

    # Numeric solution via trigonometric form for depressed cubic x^3 - 27x + 2V = 0
    V_float = float(V)
    arg = max(-1.0, min(1.0, -V_float / 27.0))
    theta = acos(arg)

    numeric_best = None
    for k in (0, 1, 2):
        x = 6.0 * cos((theta + 2 * pi * k) / 3.0)
        if x > 1e-15:
            s1 = (3.0 * x * x + 27.0) / (2.0 * x)
            r2 = (s1 * s1 - 54.0) / 4.0
            if numeric_best is None or r2 > numeric_best:
                numeric_best = r2

    # Prefer exact if it matches numeric within tolerance
    if exact_candidates:
        best_exact = max(exact_candidates).limit_denominator()
        if numeric_best is None or float(best_exact) >= numeric_best - 1e-10:
            return best_exact.numerator + best_exact.denominator

    r2_frac = Fraction(numeric_best).limit_denominator(10**6)
    return r2_frac.numerator + r2_frac.denominator

volume = 23
solve(volume)

# 调用 solve
result = solve(inputs['volume'])
print(result)