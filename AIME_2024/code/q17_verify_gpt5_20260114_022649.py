inputs = {'volume': 23}

from fractions import Fraction
import math

def solve(volume):
    K = 27  # since surface area is fixed: ab+bc+ca = 27
    # Try to find exact rational roots if volume is rational
    def divisors(n):
        n = abs(n)
        if n == 0:
            return [0]
        ds = set()
        i = 1
        while i * i <= n:
            if n % i == 0:
                ds.add(i)
                ds.add(n // i)
            i += 1
        return sorted(ds)
    def rational_roots_for_fraction(V_frac):
        # Solve x^3 - K x + 2V = 0 for rational roots using Rational Root Theorem
        roots = set()
        m = V_frac.numerator
        n = V_frac.denominator
        # Multiply equation by n to clear denominator: n x^3 - K n x + 2 m = 0
        # Rational roots p/q with p | 2m and q | n
        p_candidates = divisors(2 * m)
        q_candidates = divisors(n if n != 0 else 1)
        signs = [1, -1]
        for p in p_candidates:
            for q in q_candidates:
                if q == 0:
                    continue
                for sgn in signs:
                    x = Fraction(sgn * p, q)
                    # Evaluate exactly as Fraction
                    val = x**3 - K * x + 2 * V_frac
                    if val == 0:
                        roots.add(x)
        return sorted(roots)
    # Convert volume to Fraction if possible
    if isinstance(volume, Fraction):
        V_frac = volume
    elif isinstance(volume, int):
        V_frac = Fraction(volume, 1)
    else:
        # Attempt to interpret as rational if it's a float; fallback to approximation
        try:
            V_frac = Fraction(volume).limit_denominator(10**6)
        except:
            V_frac = None
    # First, try exact rational path
    if V_frac is not None:
        rat_roots = rational_roots_for_fraction(V_frac)
        candidates = []
        for x in rat_roots:
            if x > 0:
                # y = V / x^2
                if x == 0:
                    continue
                y = V_frac / (x * x)
                if y <= 0:
                    continue
                D2 = y * y + 2 * x * x  # a^2+b^2+c^2
                candidates.append((D2, x, y))
        if candidates:
            D2_max = max(candidates, key=lambda t: t[0])[0]
            r2 = D2_max / 4
            # Return p+q for reduced fraction
            r2 = r2.limit_denominator()
            return r2.numerator + r2.denominator
    # Fallback: numeric Cardano/trigonometric solution for depressed cubic x^3 + p x + q = 0
    p = -K
    q = 2 * float(volume)
    # Discriminant
    Delta = (q / 2) ** 2 + (p / 3) ** 3
    roots = []
    def cbrt(z):
        return math.copysign(abs(z) ** (1.0 / 3.0), z)
    if Delta >= 0:
        sqrtD = math.sqrt(Delta)
        u = cbrt(-q / 2 + sqrtD)
        v = cbrt(-q / 2 - sqrtD)
        roots = [u + v]
    else:
        # Three real roots
        A = math.sqrt(- (p / 3.0) ** 3)
        # Guard domain for acos
        cosphi = max(-1.0, min(1.0, -q / (2 * A)))
        phi = math.acos(cosphi)
        r = 2 * math.sqrt(-p / 3.0)
        roots = [r * math.cos((phi + 2 * math.pi * k) / 3.0) for k in range(3)]
    # Evaluate candidates
    best_D2 = -1.0
    for x in roots:
        if x > 0:
            y = float(volume) / (x * x)
            if y > 0:
                D2 = y * y + 2 * x * x
                if D2 > best_D2:
                    best_D2 = D2
    r2 = best_D2 / 4.0
    # Try to express as a reduced fraction if it's effectively rational
    try:
        frac = Fraction(r2).limit_denominator(10**9)
        if abs(float(frac) - r2) < 1e-12:
            return frac.numerator + frac.denominator
    except:
        pass
    return r2

solve(23)

# 调用 solve
result = solve(inputs['volume'])
print(result)