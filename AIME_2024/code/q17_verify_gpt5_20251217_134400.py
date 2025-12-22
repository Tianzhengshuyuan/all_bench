inputs = {'volume': 23}

from fractions import Fraction
from math import sqrt, acos, cos, pi


def solve(volume):
    V = Fraction(volume)
    S_pair = Fraction(27)  # ab + bc + ca = 27 from surface area 54

    # We consider extremal boxes with two equal sides: a = b = x, c = y
    # Constraints:
    #   x^2 + 2xy = 27
    #   x^2 y = V
    # Eliminating y gives cubic for x: x^3 - S_pair * x + 2V = 0

    def cbrt(x):
        return (abs(x) ** (1.0 / 3.0)) * (1 if x >= 0 else -1)

    def r2_from_x(x):
        # returns (float_value, Fraction_or_None)
        if isinstance(x, Fraction):
            if x <= 0:
                return None
            y = V / (x * x)
            s = y + 2 * x  # a + b + c
            a2b2c2 = s * s - 2 * S_pair
            r2 = a2b2c2 / 4
            return float(r2), r2
        else:
            x = float(x)
            if x <= 0:
                return None
            y = float(V) / (x * x)
            s = y + 2.0 * x
            a2b2c2 = s * s - 2.0 * float(S_pair)
            r2 = a2b2c2 / 4.0
            return r2, None

    candidates = []

    # Try to find a positive integer root via Rational Root Theorem when 2V is integer
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
            # check positive divisor r
            if r ** 3 - S_pair * r + twoV == 0:
                candidates.append(Fraction(r))
                # The other two roots come from quadratic factor x^2 + r x + (r^2 - S_pair) = 0
                disc = r * r - 4 * (r * r - S_pair)  # = 4*S_pair - 3*r^2
                if disc > 0:
                    x2 = (-r + sqrt(float(disc))) / 2.0
                    if x2 > 0:
                        candidates.append(x2)

    # If no candidates yet, solve cubic numerically for positive roots
    if not candidates:
        # Solve x^3 + p x + q = 0 with p = -S_pair, q = 2V
        p = -float(S_pair)
        q = float(2 * V)
        Delta = (q / 2.0) ** 2 + (p / 3.0) ** 3
        if Delta > 0:
            # one real root
            A = -q / 2.0
            B = sqrt(Delta)
            x = cbrt(A + B) + cbrt(A - B)
            if x > 0:
                candidates.append(x)
        else:
            # three real roots
            m = (float(S_pair) / 3.0) ** 0.5  # = sqrt(-p/3)
            arg = -q / (2.0 * m ** 3)
            arg = max(-1.0, min(1.0, arg))
            phi = acos(arg)
            for k in range(3):
                x = 2.0 * m * cos((phi + 2.0 * pi * k) / 3.0)
                if x > 1e-12:
                    candidates.append(x)

    # Evaluate candidates and select the maximal r^2
    best_val = None
    best_frac = None
    for x in candidates:
        res = r2_from_x(x if isinstance(x, Fraction) else float(x))
        if res is None:
            continue
        val, frac_val = res
        if best_val is None or val > best_val:
            best_val = val
            best_frac = frac_val

    # If we have exact fraction, return p+q
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