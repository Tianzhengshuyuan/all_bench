inputs = {'volume': 23}

from fractions import Fraction
from math import sqrt, acos, cos, pi, isfinite


def solve(volume):
    V = Fraction(volume)
    S_pair = 27  # ab + bc + ca = 27 from surface area 54

    # For extremal (maximal diagonal) box we may take a = b = x, c = y.
    # Constraints:
    #   x^2 + 2xy = S_pair
    #   x^2 y = V
    # Eliminating y gives: x^3 - S_pair * x + 2V = 0

    def r2_from_x(x):
        # Given x>0, y = V/x^2, r^2 = ((a^2+b^2+c^2))/4 = (((a+b+c)^2 - 2(ab+bc+ca)))/4
        # with a=b=x, c=y
        if isinstance(x, Fraction):
            if x <= 0:
                return None, None
            y = V / (x * x)
            s = 2 * x + y
            a2b2c2 = s * s - 2 * S_pair
            r2 = a2b2c2 / 4
            return float(r2), r2
        else:
            x = float(x)
            if not isfinite(x) or x <= 0:
                return None, None
            y = float(V) / (x * x)
            s = 2.0 * x + y
            a2b2c2 = s * s - 2.0 * S_pair
            r2 = a2b2c2 / 4.0
            return r2, None

    candidates = []

    # Try to find integer rational roots via Rational Root Theorem when 2V is integer
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
            # positive divisor r
            # Check if r is a root of x^3 - S_pair x + 2V = 0
            if r ** 3 - S_pair * r + twoV == 0:
                # exact rational root
                candidates.append(Fraction(r))
                # Other two roots from quadratic factor: x^2 + r x + (r^2 - S_pair) = 0
                disc = r * r - 4 * (r * r - S_pair)  # = 4*S_pair - 3*r^2
                if disc > 0:
                    x2 = (-r + sqrt(float(disc))) / 2.0
                    if x2 > 0:
                        candidates.append(x2)

    # If no candidates (or to ensure completeness), solve cubic numerically
    if not candidates:
        # Solve x^3 + p x + q = 0 with p = -S_pair, q = 2V
        p = -float(S_pair)
        q = float(2 * V)
        Delta = (q / 2.0) ** 2 + (p / 3.0) ** 3
        if Delta > 0:
            # one real root
            def cbrt(x):
                return (abs(x) ** (1.0 / 3.0)) * (1 if x >= 0 else -1)

            A = -q / 2.0
            B = sqrt(Delta)
            x = cbrt(A + B) + cbrt(A - B)
            if x > 0:
                candidates.append(x)
        else:
            # three real roots
            m = (S_pair / 3.0) ** 0.5  # = sqrt(-p/3)
            arg = -q / (2.0 * m ** 3)
            if arg < -1.0:
                arg = -1.0
            elif arg > 1.0:
                arg = 1.0
            phi = acos(arg)
            for k in range(3):
                x = 2.0 * m * cos((phi + 2.0 * pi * k) / 3.0)
                if x > 1e-12:
                    candidates.append(x)

    # Evaluate candidates and pick the maximal r^2
    best_val = None
    best_frac = None
    seen = []

    for x in candidates:
        # de-duplicate close numeric candidates
        xf = float(x) if isinstance(x, Fraction) else float(x)
        if any(abs(xf - y) < 1e-12 for y in seen):
            continue
        seen.append(xf)

        val, frac_val = r2_from_x(x)
        if val is None:
            continue
        if best_val is None or val > best_val + 1e-12:
            best_val = val
            best_frac = frac_val

    # If we have an exact fraction, return p+q
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