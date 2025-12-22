inputs = {'volume': 23}

from fractions import Fraction
from math import sqrt, acos, cos, pi, isfinite, isclose

def solve(volume):
    V = Fraction(volume)
    P = Fraction(27)  # ab + bc + ca = 27

    # For extremum, assume a=b=x, c=y.
    # Constraints: x^2 + 2xy = P, x^2 y = V -> y = V/x^2
    # Eliminating y: x^3 - P x + 2V = 0

    def r2_from_x_float(x):
        # r^2 = (a^2 + b^2 + c^2)/4 = (2x^2 + y^2)/4 with y=V/x^2
        y = float(V) / (x * x)
        return (2.0 * x * x + y * y) / 4.0

    def r2_from_x_exact_int(x_int):
        # exact r^2 as Fraction for integer root x_int
        y = V / (x_int * x_int)
        return (Fraction(2 * x_int * x_int, 1) + y * y) / 4

    def divisors(n):
        n = abs(n)
        ds = set()
        d = 1
        while d * d <= n:
            if n % d == 0:
                ds.add(d)
                ds.add(n // d)
            d += 1
        return sorted(ds)

    def cbrt(z):
        return (abs(z) ** (1.0 / 3.0)) * (1 if z >= 0 else -1)

    candidates = []  # float roots > 0
    best_exact = None  # Fraction for exact r^2 if available

    # Try integer roots via Rational Root Theorem when 2V is integer
    twoV = 2 * V
    if twoV.denominator == 1:
        C = abs(twoV.numerator)
        integer_roots = []
        for r in divisors(C):
            for rr in (r, -r):
                if Fraction(rr, 1) ** 3 - P * Fraction(rr, 1) + 2 * V == 0:
                    integer_roots.append(rr)

        for r in integer_roots:
            # add integer root as candidate
            if r > 0:
                candidates.append(float(r))
                r2_frac = r2_from_x_exact_int(r)
                if best_exact is None or float(r2_frac) > float(best_exact):
                    best_exact = r2_frac
            # add companion quadratic roots from factorization
            # quotient: x^2 + r x + (r^2 - P) = 0 -> discriminant D = 4P - 3r^2
            D = 4 * float(P) - 3.0 * (r * r)
            if D > 0:
                x1 = (-r + sqrt(D)) / 2.0
                x2 = (-r - sqrt(D)) / 2.0
                if x1 > 1e-12 and isfinite(x1):
                    candidates.append(x1)
                if x2 > 1e-12 and isfinite(x2):
                    candidates.append(x2)

    # If still no candidates (no integer roots found), solve cubic numerically
    if not candidates:
        p = -float(P)
        q = float(twoV)
        Delta = (q / 2.0) ** 2 + (p / 3.0) ** 3

        if Delta > 0:
            # one real root
            A = -q / 2.0
            B = sqrt(Delta)
            x = cbrt(A + B) + cbrt(A - B)
            if x > 1e-12 and isfinite(x):
                candidates.append(x)
        else:
            # three real roots
            m = (float(P) / 3.0) ** 0.5  # sqrt(-p/3) = sqrt(P/3)
            arg = -q / (2.0 * m ** 3)
            arg = max(-1.0, min(1.0, arg))
            phi = acos(arg)
            for k in range(3):
                x = 2.0 * m * cos((phi + 2.0 * pi * k) / 3.0)
                if x > 1e-12 and isfinite(x):
                    candidates.append(x)

    # Deduplicate numeric candidates
    uniq = []
    for x in candidates:
        if not any(isclose(x, y, rel_tol=1e-12, abs_tol=1e-12) for y in uniq):
            uniq.append(x)

    if not uniq:
        return None

    # Evaluate r^2 over candidates, take the maximum
    best_float = max(r2_from_x_float(x) for x in uniq)

    # Prefer exact fraction if it matches/exceeds numeric best (within tolerance)
    if best_exact is not None and float(best_exact) >= best_float - 1e-12:
        r2 = best_exact.limit_denominator()
        return r2.numerator + r2.denominator

    # Fallback: approximate numeric best as a fraction
    approx = Fraction(best_float).limit_denominator(10 ** 12)
    return approx.numerator + approx.denominator

# 调用 solve
result = solve(inputs['volume'])
print(result)