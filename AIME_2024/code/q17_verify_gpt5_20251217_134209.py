inputs = {'volume': 23}

from fractions import Fraction
from math import sqrt, acos, cos, pi, isclose


def solve(volume):
    V = Fraction(volume)
    S_pair = 27  # ab + bc + ca = 27

    # We consider extremal boxes with two equal sides: a = b = x, c = y
    # Constraints:
    #   x^2 + 2xy = 27
    #   x^2 y = V
    # Eliminating y gives cubic: x^3 - S_pair * x + 2V = 0
    def divisors(n):
        n = abs(n)
        divs = set()
        d = 1
        while d * d <= n:
            if n % d == 0:
                divs.add(d)
                divs.add(n // d)
            d += 1
        return sorted(divs)

    def cbrt(x):
        if x >= 0:
            return x ** (1.0 / 3.0)
        else:
            return -((-x) ** (1.0 / 3.0))

    # Compute r^2 for a candidate x; return as (float_value, Fraction_or_None)
    def r2_from_x(x_val, is_fraction):
        if is_fraction:
            x = Fraction(x_val)
            if x <= 0:
                return None
            y = V / (x * x)
            s1 = y + 2 * x  # a + b + c
            S_sum_sq = s1 * s1 - 2 * S_pair  # a^2 + b^2 + c^2
            r2 = S_sum_sq / 4
            return float(r2), r2
        else:
            x = float(x_val)
            if x <= 0:
                return None
            y = float(V) / (x * x)
            s1 = y + 2.0 * x
            S_sum_sq = s1 * s1 - 2.0 * S_pair
            r2 = S_sum_sq / 4.0
            return r2, None

    candidates = []

    # Try to find integer positive roots by Rational Root Theorem when 2V is integer
    if (2 * V).denominator == 1:
        twoV = int(2 * V)
        for d in divisors(twoV):
            for cand in (d, -d):
                if cand > 0 and cand ** 3 - S_pair * cand + twoV == 0:
                    # integer root found
                    candidates.append(("frac", Fraction(cand)))
                    # other roots from quadratic factor: x^2 + r x + (r^2 - S) = 0
                    r = cand
                    disc = r * r - 4 * (r * r - S_pair)  # = 4*S - 3*r^2
                    if disc > 0:
                        # positive root is (-r + sqrt(disc)) / 2
                        x2 = (-r + sqrt(disc)) / 2.0
                        if x2 > 0:
                            candidates.append(("float", x2))

    # If no integer root found, solve cubic numerically for all positive real roots
    if not candidates:
        # Solve x^3 + p x + q = 0 with p = -S_pair, q = 2V
        p = -float(S_pair)
        q = float(2 * V)
        # Discriminant for depressed cubic: Δ = (q/2)^2 + (p/3)^3
        Delta = (q / 2.0) ** 2 + (p / 3.0) ** 3
        if Delta > 0:
            # one real root
            A = -q / 2.0
            B = sqrt(Delta)
            x = cbrt(A + B) + cbrt(A - B)
            if x > 0:
                candidates.append(("float", x))
        else:
            # three real roots (Delta <= 0, including casus irreducibilis)
            m = (S_pair / 3.0) ** 0.5
            # guard domain of acos
            arg = -q / (2.0 * m ** 3)
            if arg < -1:
                arg = -1.0
            elif arg > 1:
                arg = 1.0
            phi = acos(arg)
            for k in range(3):
                x = 2.0 * m * cos((phi + 2.0 * pi * k) / 3.0)
                if x > 1e-12:
                    candidates.append(("float", x))

    # Evaluate candidates and select the maximal r^2
    best_val = None
    best_frac = None
    for typ, x in candidates:
        res = r2_from_x(x, is_fraction=(typ == "frac"))
        if res is None:
            continue
        val, frac_val = res
        if best_val is None or val > best_val + 1e-12:
            best_val = val
            best_frac = frac_val
        elif isclose(val, best_val, rel_tol=1e-12, abs_tol=1e-12) and best_frac is None and frac_val is not None:
            # prefer exact fraction if tied
            best_frac = frac_val

    # If we have exact fraction, return p+q
    if best_frac is not None:
        r2 = best_frac.limit_denominator()  # ensure reduced
        return r2.numerator + r2.denominator

    # Fallback: approximate best_val as a fraction
    if best_val is not None:
        approx = Fraction(best_val).limit_denominator(10 ** 9)
        return approx.numerator + approx.denominator

    return None

# 调用 solve
result = solve(inputs['volume'])
print(result)