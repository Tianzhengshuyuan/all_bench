inputs = {'surface_area': 54}

from fractions import Fraction
import math

def solve(surface_area):
    V = Fraction(23, 1)
    s2 = Fraction(surface_area, 2)  # ab + bc + ca

    # In the extremal case, two sides are equal: let b = c = x, a = y = V/x^2
    # Constraint reduces to cubic: x^3 - s2*x + 2V = 0
    def r2_from_x(x):
        y = float(V) / (x * x)
        return (y * y + 2 * x * x) / 4.0

    def cbrt(z):
        return math.copysign(abs(z) ** (1 / 3), z)

    # Solve depressed cubic x^3 + p x + q = 0 with p = -s2, q = 2V
    p = -float(s2)
    q = float(2 * V)
    D = (q / 2) ** 2 + (p / 3) ** 3

    roots = []
    eps = 1e-15
    if D > eps:
        s = math.sqrt(D)
        u = cbrt(-q / 2 + s)
        v = cbrt(-q / 2 - s)
        roots = [u + v]
    elif D < -eps:
        base = -p / 3
        rmag = 2 * math.sqrt(base) if base > 0 else 0.0
        denom = math.sqrt(base ** 3) if base > 0 else 1.0
        arg = (-q / 2) / denom if denom != 0 else 1.0
        arg = max(-1.0, min(1.0, arg))
        theta = math.acos(arg)
        roots = [rmag * math.cos((theta + 2 * math.pi * k) / 3) for k in range(3)]
    else:
        u = cbrt(-q / 2)
        roots = [2 * u, -u]

    # Evaluate r^2 for positive roots and take maximum
    best_r2 = None
    for x in roots:
        if x > 1e-14:
            r2 = r2_from_x(x)
            if best_r2 is None or r2 > best_r2:
                best_r2 = r2

    # Convert to fraction and return p+q
    frac = Fraction(best_r2).limit_denominator(10**12)
    return frac.numerator + frac.denominator

solve(54)

# 调用 solve
result = solve(inputs['surface_area'])
print(result)