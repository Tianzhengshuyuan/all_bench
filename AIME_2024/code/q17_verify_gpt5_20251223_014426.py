inputs = {'surface_area': 54}

from math import sqrt, acos, cos, pi, copysign
from fractions import Fraction

def solve(surface_area):
    V = 23  # fixed volume from the problem

    def cbrt(x):
        return copysign(abs(x) ** (1/3), x)

    def real_cubic_roots(p, q):
        # Solve x^3 + p x + q = 0
        D = (q/2)**2 + (p/3)**3
        eps = 1e-14
        if D > eps:
            s = sqrt(D)
            u = cbrt(-q/2 + s)
            v = cbrt(-q/2 - s)
            return [u + v]
        elif D < -eps:
            r = 2 * sqrt(-p/3)
            theta = acos(max(-1.0, min(1.0, (-q/2) / sqrt(-(p/3)**3))))
            return [r * cos((theta + 2*k*pi) / 3) for k in range(3)]
        else:
            u = cbrt(-q/2)
            return [2*u, -u]

    S = float(surface_area)
    p = -(S / 2.0)
    q = 2.0 * V
    roots = real_cubic_roots(p, q)

    # Choose positive roots only and compute corresponding r^2
    candidates = []
    for x in roots:
        if x > 1e-12:
            y = V / (x * x)
            d2 = 2 * (x * x) + y * y
            r2 = d2 / 4.0
            candidates.append((r2, x))

    if not candidates:
        return None

    r2_val, x_sel = max(candidates, key=lambda t: t[0])

    # Try to return p+q if r^2 is rational (as in the original problem).
    # We detect a rational x via exact check on the cubic using Fractions.
    if isinstance(surface_area, int):
        S_frac = Fraction(surface_area, 1)
    else:
        S_frac = Fraction(surface_area).limit_denominator(10**6)

    x_frac = Fraction(x_sel).limit_denominator(10**6)
    # Check if x_frac is an exact root of x^3 - (S/2)x + 2V = 0 over rationals
    if x_frac**3 - (S_frac / 2) * x_frac + Fraction(2 * V, 1) == 0:
        y_frac = Fraction(V, 1) / (x_frac * x_frac)
        d2_frac = 2 * (x_frac * x_frac) + (y_frac * y_frac)
        r2_frac = d2_frac / 4
        return r2_frac.numerator + r2_frac.denominator

    # Fallback: return numeric r^2 if not rational
    return r2_val

solve(surface_area)

# 调用 solve
result = solve(inputs['surface_area'])
print(result)