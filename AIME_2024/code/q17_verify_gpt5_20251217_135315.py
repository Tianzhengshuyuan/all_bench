inputs = {'volume': 23}

from fractions import Fraction
from math import sqrt, acos, cos, pi, isfinite


def solve(volume):
    V = Fraction(volume)
    S = 27  # ab + bc + ca = 27 since surface area is 54

    # For extremal (maximal diagonal) box take b = c = x, a = y:
    #   x^2 + 2xy = S
    #   x^2 y = V -> y = V / x^2
    # Eliminating y gives cubic in x:
    #   x^3 - S x + 2V = 0

    def r2_from_x_float(x):
        y = float(V) / (x * x)
        return (2.0 * x * x + y * y) / 4.0

    best_float = None
    best_exact = None
    candidates = []

    # Try rational root (integer) when 2V is integer
    twoV = 2 * V
    if twoV.denominator == 1:
        C = abs(twoV.numerator)
        divs = set()
        d = 1
        while d * d <= C:
            if C % d == 0:
                divs.add(d)
                divs.add(C // d)
            d += 1

        integer_roots = []
        for r in sorted(divs):
            for rr in (r, -r):
                if rr ** 3 - S * rr + twoV == 0:
                    integer_roots.append(rr)

        # Process integer roots and companion quadratic roots
        for r in integer_roots:
            # integer root itself
            if r > 0:
                candidates.append(float(r))
                # exact r^2 for integer x = r
                y = V / (r * r)
                r2_frac = (Fraction(2 * r * r, 1) + y * y) / 4
                if best_exact is None or float(r2_frac) > float(best_exact):
                    best_exact = r2_frac
            # companion roots from quadratic factor: x^2 + r x + (r^2 - S) = 0
            D = r * r - 4 * (r * r - S)  # 4S - 3r^2
            if D > 0:
                x1 = (-r + sqrt(D)) / 2.0
                x2 = (-r - sqrt(D)) / 2.0
                if x1 > 1e-12:
                    candidates.append(x1)
                if x2 > 1e-12:
                    candidates.append(x2)

    # If no candidates yet, solve cubic numerically
    if not candidates:
        p = -float(S)
        q = float(twoV)
        Delta = (q / 2.0) ** 2 + (p / 3.0) ** 3

        def cbrt(z):
            return (abs(z) ** (1.0 / 3.0)) * (1 if z >= 0 else -1)

        if Delta > 0:
            A = -q / 2.0
            B = sqrt(Delta)
            x = cbrt(A + B) + cbrt(A - B)
            if x > 1e-12 and isfinite(x):
                candidates.append(x)
        else:
            m = (S / 3.0) ** 0.5  # sqrt(-p/3)
            arg = -q / (2.0 * m ** 3)
            if arg < -1.0:
                arg = -1.0
            elif arg > 1.0:
                arg = 1.0
            phi = acos(arg)
            for k in range(3):
                x = 2.0 * m * cos((phi + 2.0 * pi * k) / 3.0)
                if x > 1e-12 and isfinite(x):
                    candidates.append(x)

    # Evaluate r^2 over candidates, take maximum
    seen = []
    for x in candidates:
        xf = float(x)
        if any(abs(xf - s) < 1e-12 for s in seen):
            continue
        seen.append(xf)
        val = r2_from_x_float(xf)
        if best_float is None or val > best_float:
            best_float = val

    # Prefer exact fraction if it matches or exceeds numeric best
    if best_exact is not None:
        if best_float is None or float(best_exact) >= best_float - 1e-12:
            r2 = best_exact.limit_denominator()
            return r2.numerator + r2.denominator

    # Fallback: approximate numeric best as a fraction
    if best_float is not None:
        approx = Fraction(best_float).limit_denominator(10 ** 9)
        return approx.numerator + approx.denominator

    return None

# 调用 solve
result = solve(inputs['volume'])
print(result)