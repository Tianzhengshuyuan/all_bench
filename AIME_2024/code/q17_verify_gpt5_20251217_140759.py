inputs = {'volume': 23}

from fractions import Fraction
from math import sqrt, acos, cos, pi, isfinite, isclose

def solve(volume):
    V = Fraction(volume)
    S_pair = Fraction(27)  # ab + bc + ca = 27 since surface area is 54

    # Extremal (maximal diagonal) box occurs with two equal sides: let a=b=x, c=y
    # Constraints:
    #   x^2 + 2xy = S_pair
    #   x^2 y = V  => y = V / x^2
    # Eliminating y gives cubic in x:
    #   x^3 - S_pair * x + 2V = 0

    def cbrt(z):
        return (abs(z) ** (1.0 / 3.0)) * (1 if z >= 0 else -1)

    def r2_from_x_float(x):
        # r^2 = (a^2 + b^2 + c^2)/4 = (2x^2 + y^2)/4 with y = V/x^2
        y = float(V) / (x * x)
        return (2.0 * x * x + y * y) / 4.0

    def r2_from_x_exact_int(x_int):
        # exact r^2 as Fraction for integer root x_int
        y = V / (x_int * x_int)
        return (Fraction(2 * x_int * x_int, 1) + y * y) / 4

    # Solve cubic x^3 - S_pair x + 2V = 0 numerically to get positive real roots
    def positive_roots():
        roots = []
        p = -float(S_pair)
        q = float(2 * V)
        Delta = (q / 2.0) ** 2 + (p / 3.0) ** 3
        if Delta > 0:
            # one real root
            A = -q / 2.0
            B = sqrt(Delta)
            x = cbrt(A + B) + cbrt(A - B)
            if x > 1e-12 and isfinite(x):
                roots.append(x)
        else:
            # three real roots
            m = (float(S_pair) / 3.0) ** 0.5  # sqrt(-p/3) = sqrt(S/3)
            arg = -q / (2.0 * m ** 3)
            arg = max(-1.0, min(1.0, arg))
            phi = acos(arg)
            for k in range(3):
                x = 2.0 * m * cos((phi + 2.0 * pi * k) / 3.0)
                if x > 1e-12 and isfinite(x):
                    roots.append(x)
        # de-duplicate
        uniq = []
        for x in roots:
            if not any(isclose(x, y, rel_tol=1e-12, abs_tol=1e-12) for y in uniq):
                uniq.append(x)
        return uniq

    # Get numeric best r^2
    roots = positive_roots()
    if not roots:
        return None
    best_r2_float = max(r2_from_x_float(x) for x in roots)

    # Try integer root for exact rational r^2 (via Rational Root Theorem on monic cubic)
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
            for rr in (r, -r):
                if rr ** 3 - S_pair * rr + twoV == 0:
                    # exact integer root
                    if rr > 0:
                        r2_exact = r2_from_x_exact_int(rr)
                        if best_r2_exact is None or float(r2_exact) > float(best_r2_exact):
                            best_r2_exact = r2_exact

    if best_r2_exact is not None and float(best_r2_exact) >= best_r2_float - 1e-12:
        r2 = best_r2_exact.limit_denominator()
        return r2.numerator + r2.denominator

    # Fallback: approximate numeric best as a fraction
    approx = Fraction(best_r2_float).limit_denominator(10 ** 12)
    return approx.numerator + approx.denominator

# 调用 solve
result = solve(inputs['volume'])
print(result)