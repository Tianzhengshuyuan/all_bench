inputs = {'volume': 23}

from fractions import Fraction
from math import sqrt, acos, cos, pi


def solve(volume):
    V = Fraction(volume)
    S_pair = 27  # ab + bc + ca = 27 since surface area is 54

    # At the extremum (max diagonal), two sides are equal: let a = b = x, c = y
    # Constraints:
    #   x^2 + 2xy = S_pair
    #   x^2 y = V  => y = V / x^2
    # Eliminating y gives cubic in x:
    #   x^3 - S_pair * x + 2V = 0

    def r2_from_x(x):
        # r^2 = (a^2 + b^2 + c^2)/4 = (2x^2 + y^2)/4 with y = V/x^2
        y = V / (x * x)
        return (2 * x * x + y * y) / 4

    # Find all positive real roots of x^3 - S_pair x + 2V = 0
    roots = []

    # Depressed cubic: x^3 + p x + q = 0 with p = -S_pair, q = 2V
    p = -float(S_pair)
    q = float(2 * V)
    Delta = (q / 2.0) ** 2 + (p / 3.0) ** 3

    def cbrt(z):
        return (abs(z) ** (1.0 / 3.0)) * (1 if z >= 0 else -1)

    if Delta > 0:
        # One real root
        A = -q / 2.0
        B = sqrt(Delta)
        x = cbrt(A + B) + cbrt(A - B)
        if x > 1e-12:
            roots.append(x)
    else:
        # Three real roots
        m = (S_pair / 3.0) ** 0.5  # sqrt(-p/3)
        arg = (-q) / (2.0 * m ** 3)
        # clamp for numerical safety
        arg = max(-1.0, min(1.0, arg))
        phi = acos(arg)
        for k in range(3):
            x = 2.0 * m * cos((phi + 2.0 * pi * k) / 3.0)
            if x > 1e-12:
                roots.append(x)

    # Evaluate r^2 for positive roots, track maximum (float)
    best_r2_float = None
    for x in roots:
        y = float(V) / (x * x)
        r2 = (2.0 * x * x + y * y) / 4.0
        if best_r2_float is None or r2 > best_r2_float:
            best_r2_float = r2

    # Try to detect exact rational case via an integer root (Rational Root Theorem)
    best_r2_exact = None
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
        for r in sorted(divs):
            # Check r as an integer root
            if r ** 3 - S_pair * r + twoV == 0:
                # exact positive integer root
                x_exact = Fraction(r)
                r2_exact = r2_from_x(x_exact)
                # Compare with best float to decide if this is the maximizing root
                if best_r2_float is None or float(r2_exact) >= best_r2_float - 1e-12:
                    if best_r2_exact is None or float(r2_exact) > float(best_r2_exact):
                        best_r2_exact = r2_exact

    if best_r2_exact is not None:
        r2 = best_r2_exact.limit_denominator()
        return r2.numerator + r2.denominator

    # Fallback: approximate as fraction
    if best_r2_float is not None:
        approx = Fraction(best_r2_float).limit_denominator(10 ** 9)
        return approx.numerator + approx.denominator

    return None

# 调用 solve
result = solve(inputs['volume'])
print(result)