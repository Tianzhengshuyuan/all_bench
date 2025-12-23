inputs = {'surface_area': 54}

from fractions import Fraction
import math

def solve(surface_area):
    S = Fraction(surface_area, 1)  # surface area
    V = Fraction(23, 1)            # fixed volume

    # At the extremum, two sides are equal: let (x, x, y) with y = V/x^2.
    # From surface constraint ab+bc+ca = S/2: x^2 + 2xy = S/2 -> x^3 - (S/2)x + 2V = 0

    # Build integer-coefficient cubic A x^3 + C x + D = 0 equivalent to x^3 - (S/2)x + 2V = 0
    sigma2 = S / 2
    a, b = sigma2.numerator, sigma2.denominator
    n, d = V.numerator, V.denominator
    A = b * d
    C = -a * d
    D = 2 * b * n

    def divisors(N):
        N = abs(int(N))
        res = set()
        i = 1
        while i * i <= N:
            if N % i == 0:
                res.add(i)
                res.add(N // i)
            i += 1
        return sorted(res)

    # Try rational roots via Rational Root Theorem
    rational_roots = set()
    for p in divisors(D):
        for q in divisors(A):
            for sgn in (1, -1):
                x = Fraction(sgn * p, q)
                if x > 0 and A * x**3 + C * x + D == 0:
                    rational_roots.add(x)

    # Evaluate r^2 = (2x^2 + y^2)/4 with y = V/x^2 for rational roots
    best_r2_frac = None
    for x in rational_roots:
        y = V / (x * x)
        r2 = Fraction(1, 4) * (2 * x * x + y * y)
        if best_r2_frac is None or r2 > best_r2_frac:
            best_r2_frac = r2

    # Solve cubic numerically for completeness: x^3 - sigma2 x + 2V = 0
    p_dep = -float(sigma2)
    q_dep = 2.0 * float(V)
    Delta = (q_dep / 2.0) ** 2 + (p_dep / 3.0) ** 3

    def cbrt_real(x):
        return math.copysign(abs(x) ** (1.0 / 3.0), x)

    roots = []
    eps = 1e-15
    if Delta > eps:
        u = cbrt_real(-q_dep / 2.0 + math.sqrt(Delta))
        v = cbrt_real(-q_dep / 2.0 - math.sqrt(Delta))
        roots = [u + v]
    elif abs(Delta) <= eps:
        u = cbrt_real(-q_dep / 2.0)
        roots = [2.0 * u, -u, -u]
    else:
        R = 2.0 * math.sqrt(-p_dep / 3.0)
        denom = math.sqrt((-p_dep / 3.0) ** 3)
        val = (-q_dep / 2.0) / denom
        val = max(-1.0, min(1.0, val))
        phi = math.acos(val)
        roots = [R * math.cos((phi + 2.0 * math.pi * k) / 3.0) for k in range(3)]

    # Evaluate r^2 numerically for positive roots and take maximum
    best_r2_num = None
    for x in roots:
        if x > 0:
            y = float(V) / (x * x)
            r2 = 0.25 * (2.0 * x * x + y * y)
            if best_r2_num is None or r2 > best_r2_num:
                best_r2_num = r2

    # Prefer exact rational if available; otherwise approximate as a rational
    if best_r2_frac is not None:
        r2_final = best_r2_frac
    else:
        r2_final = Fraction(best_r2_num).limit_denominator(10**12)

    return r2_final.numerator + r2_final.denominator

solve(surface_area)

# 调用 solve
result = solve(inputs['surface_area'])
print(result)