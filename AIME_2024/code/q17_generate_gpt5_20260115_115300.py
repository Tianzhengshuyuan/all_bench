inputs = {'surface_area': 94}

from fractions import Fraction
import math

def solve(surface_area):
    V = 23  # fixed volume from the problem

    # Try to find rational positive roots of 2a^3 - S a + 4V = 0 using Rational Root Theorem
    roots = []
    S = surface_area

    def divisors(n):
        n = abs(int(n))
        ds = set()
        for i in range(1, int(n**0.5) + 1):
            if n % i == 0:
                ds.add(i)
                ds.add(n // i)
        return sorted(ds)

    if isinstance(S, int):
        A = 2
        C = -S
        D = 4 * V
        p_divs = divisors(D)
        q_divs = divisors(A)
        cand_set = set()
        for p in p_divs:
            for q in q_divs:
                for sign in (-1, 1):
                    cand = Fraction(sign * p, q)
                    val = Fraction(A) * cand**3 + Fraction(C) * cand + Fraction(D)
                    if val == 0:
                        if cand > 0:
                            roots.append(cand)
        # deduplicate
        roots = sorted(set(roots))

    if roots:
        best_r2 = None
        for a in roots:
            L = Fraction(V, 1) / (a * a)
            d2 = 2 * (a * a) + (Fraction(V, 1) ** 2) / (a ** 4)
            r2 = d2 / 4
            if best_r2 is None or r2 > best_r2:
                best_r2 = r2
        return best_r2.numerator + best_r2.denominator
    else:
        # Numeric fallback: solve depressed cubic a^3 + p a + q = 0 with p = -S/2, q = 2V
        p = -S / 2.0
        q = 2.0 * V
        delta = (q / 2.0) ** 2 + (p / 3.0) ** 3

        def cbrt(x):
            return math.copysign(abs(x) ** (1.0 / 3.0), x)

        real_roots = []
        if delta > 0:
            u = cbrt(-q / 2.0 + math.sqrt(delta))
            v = cbrt(-q / 2.0 - math.sqrt(delta))
            x = u + v
            if x > 0:
                real_roots.append(x)
        else:
            r = math.sqrt(- (p / 3.0) ** 3) if p != 0 else 0.0
            if r == 0:
                x = cbrt(-q)
                if x > 0:
                    real_roots.append(x)
            else:
                phi = math.acos(max(-1.0, min(1.0, -q / (2.0 * r))))
                m = 2.0 * math.sqrt(-p / 3.0)
                for k in range(3):
                    x = m * math.cos((phi + 2 * math.pi * k) / 3.0)
                    if x > 0:
                        real_roots.append(x)

        # Deduplicate numerically
        uniq_roots = []
        for x in real_roots:
            if not any(abs(x - y) < 1e-12 for y in uniq_roots):
                uniq_roots.append(x)

        max_r2 = None
        for a in uniq_roots:
            d2 = 2 * (a * a) + (V * V) / (a ** 4)
            r2 = d2 / 4.0
            if max_r2 is None or r2 > max_r2:
                max_r2 = r2

        if max_r2 is None:
            return None  # should not happen for valid inputs

        frac_r2 = Fraction(max_r2).limit_denominator(10**12)
        return frac_r2.numerator + frac_r2.denominator

solve(54)

# 调用 solve
result = solve(inputs['surface_area'])
print(result)