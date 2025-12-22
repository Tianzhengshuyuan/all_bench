inputs = {'volume': 23}

from fractions import Fraction
from math import sqrt, acos, cos, pi


def solve(volume):
    V = Fraction(volume)
    S_pair = Fraction(27)  # ab + bc + ca = 27 (since surface area is 54)

    # At the extremum, two sides are equal: let a = b = x, c = y.
    # Constraints:
    #   x^2 + 2xy = S_pair
    #   x^2 y = V
    # Eliminating y gives the cubic in x:
    #   x^3 - S_pair * x + 2V = 0

    def cbrt(x):
        return (abs(x) ** (1.0 / 3.0)) * (1 if x >= 0 else -1)

    def r2_from_x(x):
        # Given x > 0, y = V / x^2, r^2 = (a^2 + b^2 + c^2) / 4
        if x <= 0:
            return None, None
        y = V / (x * x)
        a2b2c2 = 2 * x * x + y * y
        r2 = a2b2c2 / 4
        return float(r2), r2 if isinstance(x, Fraction) else None

    # Collect candidate positive roots x of the cubic
    candidates = []

    # Try to find integer roots (Rational Root Theorem, monic cubic)
    twoV = 2 * V
    if twoV.denominator == 1:
        c = abs(twoV.numerator)
        divs = set()
        d = 1
        while d * d <= c:
            if c % d == 0:
                divs.add(d)
                divs.add(c // d)
            d += 1
        for r in sorted(divs):
            # Check positive integer r
            if r ** 3 - S_pair * r + twoV == 0:
                # exact integer root
                candidates.append(Fraction(r))
                # Add the other positive root from the quadratic factor (if any)
                # Quotient is x^2 + r x + (r^2 - S_pair)
                disc = r * r - 4 * (r * r - S_pair)  # = 4*S_pair - 3*r^2
                if disc > 0:
                    x2 = (-r + sqrt(float(disc))) / 2.0
                    if x2 > 0:
                        candidates.append(x2)

    # If no candidates, solve cubic numerically to get positive roots
    if not candidates:
        # Solve t^3 + p t + q = 0 with p = -S_pair, q = 2V
        p = -float(S_pair)
        q = float(2 * V)
        Delta = (q / 2.0) ** 2 + (p / 3.0) ** 3
        if Delta > 0:
            # One real root
            A = -q / 2.0
            B = sqrt(Delta)
            x = cbrt(A + B) + cbrt(A - B)
            if x > 1e-12:
                candidates.append(x)
        else:
            # Three real roots
            m = (float(S_pair) / 3.0) ** 0.5  # sqrt(-p/3)
            arg = -q / (2.0 * m ** 3)
            arg = max(-1.0, min(1.0, arg))
            phi = acos(arg)
            for k in range(3):
                x = 2.0 * m * cos((phi + 2.0 * pi * k) / 3.0)
                if x > 1e-12:
                    candidates.append(x)

    # Evaluate r^2 for all candidates and pick the maximum
    best_val = None
    best_frac = None
    seen = set()
    for x in candidates:
        xf = float(x) if isinstance(x, Fraction) else float(x)
        if any(abs(xf - s) < 1e-12 for s in seen):
            continue
        seen.add(xf)
        if isinstance(x, Fraction):
            val, frac_val = r2_from_x(x)
        else:
            val, frac_val = r2_from_x(Fraction(x).limit_denominator(10**12))
            if val is None:
                # fallback purely float
                y = float(V) / (xf * xf)
                val = (2 * xf * xf + y * y) / 4.0
                frac_val = None
        if val is None:
            continue
        if best_val is None or val > best_val + 1e-12:
            best_val = val
            best_frac = frac_val

    # Prefer exact fraction if available
    if best_frac is not None:
        r2 = best_frac.limit_denominator()
        return r2.numerator + r2.denominator

    # Fallback: approximate as fraction
    if best_val is not None:
        approx = Fraction(best_val).limit_denominator(10 ** 9)
        return approx.numerator + approx.denominator

    return None

# 调用 solve
result = solve(inputs['volume'])
print(result)