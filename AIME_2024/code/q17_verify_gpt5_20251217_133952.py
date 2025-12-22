inputs = {'volume': 23}

from fractions import Fraction
from math import sqrt, acos, cos, pi


def solve(volume):
    V = Fraction(volume)
    # Given surface area 54 => ab + bc + ca = 27
    S_pair = 27

    # Assume extremal box has two equal sides: let x, x, y
    # Constraints:
    #   x^2 + 2xy = 27
    #   x^2 y = V
    # Eliminating y: x^3 - 27 x + 2V = 0
    # Try to find an integer positive root by Rational Root Theorem
    r_pos_int_roots = []
    if V.denominator == 1:
        twoV = abs(2 * V.numerator)

        # get divisors of twoV
        divs = set()
        d = 1
        while d * d <= twoV:
            if twoV % d == 0:
                divs.add(d)
                divs.add(twoV // d)
            d += 1

        for d in sorted(divs):
            for cand in (d, -d):
                if cand > 0:
                    if cand ** 3 - S_pair * cand + 2 * V.numerator == 0:
                        r_pos_int_roots.append(cand)

    best_r2_frac = None  # best r^2 as Fraction if available
    best_r2_float = None  # best r^2 as float for fallback

    def update_best_from_x(x, rational=False):
        nonlocal best_r2_frac, best_r2_float
        if rational:
            x_int = x
            y = V / (x_int * x_int)
            s1 = y + 2 * x_int
            D2 = s1 * s1 - 2 * S_pair
            r2 = D2 / 4
            if best_r2_frac is None or float(r2) > float(best_r2_frac):
                best_r2_frac = r2
                best_r2_float = float(r2)
        else:
            if x <= 0:
                return
            y = float(V) / (x * x)
            s1 = y + 2 * x
            D2 = s1 * s1 - 2 * S_pair
            r2 = D2 / 4.0
            if best_r2_float is None or r2 > best_r2_float + 1e-15:
                best_r2_float = r2

    # Use integer root(s) if any found
    for r in set(r_pos_int_roots):
        # Candidate 1: x = r (rational path)
        update_best_from_x(r, rational=True)
        # Candidate 2: other positive root from quadratic factor
        # After factoring by (x - r): x^2 + r x + (r^2 - S) = 0
        disc = r * r - 4 * (r * r - S_pair)  # = 4 S - 3 r^2
        if disc > 0:
            x2 = (-r + sqrt(disc)) / 2.0
            update_best_from_x(x2, rational=False)

    # If no integer roots found, fall back to solving cubic numerically
    if not r_pos_int_roots:
        # Solve t^3 - S t + 2V = 0, with S = 27.
        # Depressed cubic: x^3 + p x + q = 0 with p = -S, q = 2V
        p = -S_pair
        q = float(2 * V)
        # Discriminant Δ = -4 p^3 - 27 q^2 = 4 S^3 - 108 V^2
        disc = 4 * (S_pair ** 3) - 108 * (float(V) ** 2)
        roots = []
        if disc >= 0:
            # three real roots
            m = (S_pair / 3.0) ** 0.5
            phi = acos(-q / (2 * m ** 3))
            for k in range(3):
                x = 2 * m * cos((phi + 2 * pi * k) / 3.0)
                if x > 0:
                    roots.append(x)
        else:
            # one real root via Cardano
            def cbrt(x):
                return (abs(x) ** (1 / 3.0)) * (1 if x >= 0 else -1)
            A = -q / 2.0
            B = (q / 2.0) ** 2 + (p / 3.0) ** 3
            x = cbrt(A + sqrt(B)) + cbrt(A - sqrt(B))
            if x > 0:
                roots.append(x)
        for x in roots:
            update_best_from_x(x, rational=False)

    # If we have a rational best (from integer root), return exact p+q
    if best_r2_frac is not None:
        r2 = best_r2_frac
        # ensure reduced
        r2 = Fraction(r2.numerator, r2.denominator)
        return r2.numerator + r2.denominator

    # Fallback: approximate fraction for numeric result (shouldn't happen for the given volume=23)
    if best_r2_float is not None:
        approx = Fraction(best_r2_float).limit_denominator(10 ** 6)
        return approx.numerator + approx.denominator

    # If all else fails (should not happen)
    return None

# 调用 solve
result = solve(inputs['volume'])
print(result)