inputs = {'volume': 23}

from fractions import Fraction
import math

def solve(volume):
    K = 27  # ab + bc + ca = 27 (since surface area is 54)
    # Convert volume to Fraction
    try:
        V = Fraction(volume)
    except:
        V = Fraction(float(volume)).limit_denominator(10**9)

    # Infeasible if V <= 0 or V > 27 (max at a=b=c=3)
    if V <= 0:
        return None
    if V > 27:
        return None

    # Try exact rational roots for x^3 - K x + 2V = 0 via Rational Root Theorem
    def divisors(n):
        n = abs(n)
        ds = set()
        if n == 0:
            return {0}
        i = 1
        while i * i <= n:
            if n % i == 0:
                ds.add(i)
                ds.add(n // i)
            i += 1
        return ds

    def exact_candidates_r2():
        a, b = V.numerator, V.denominator  # V = a/b in lowest terms
        roots = []
        Ps = divisors(2 * a if a != 0 else 1)
        Qs = divisors(b if b != 0 else 1)
        seen = set()
        for p in Ps:
            for q in Qs:
                for s in (1, -1):
                    x = Fraction(s * p, q)
                    if x <= 0 or x in seen:
                        continue
                    seen.add(x)
                    # Check b*x^3 - K*b*x + 2*a == 0
                    if b * x**3 - K * b * x + 2 * a == 0:
                        roots.append(x)
        # Compute r^2 for each positive rational root
        best = None
        for x in roots:
            y = V / (x * x)
            if y <= 0:
                continue
            r2 = (2 * x * x + y * y) / 4
            if best is None or r2 > best:
                best = r2
        return best

    r2_exact = exact_candidates_r2()
    if r2_exact is not None:
        r2_exact = r2_exact.limit_denominator()
        return r2_exact.numerator + r2_exact.denominator

    # Fallback: numeric Cardano/trigonometric solution
    p = -K
    q = 2 * float(V)
    Delta = (q / 2.0) ** 2 + (p / 3.0) ** 3

    def cbrt(z):
        return math.copysign(abs(z) ** (1.0 / 3.0), z)

    roots = []
    if Delta >= 0:
        sqrtD = math.sqrt(Delta)
        u = cbrt(-q / 2.0 + sqrtD)
        v = cbrt(-q / 2.0 - sqrtD)
        roots = [u + v]
    else:
        r = 2.0 * math.sqrt(-p / 3.0)
        cosphi = max(-1.0, min(1.0, -q / (2.0 * (r / 2.0) ** 3)))
        # Alternative stable form:
        phi = math.acos(max(-1.0, min(1.0, -q / (2.0 * math.sqrt((-p / 3.0) ** 3)))))
        roots = [r * math.cos((phi + 2.0 * math.pi * k) / 3.0) for k in range(3)]

    best_r2 = None
    V_float = float(V)
    for x in roots:
        if x > 1e-15:
            y = V_float / (x * x)
            if y > 0:
                r2 = (2.0 * x * x + y * y) / 4.0
                if best_r2 is None or r2 > best_r2:
                    best_r2 = r2

    if best_r2 is None:
        return None

    # Try to express best_r2 as a simple rational if possible
    r2_frac = Fraction(best_r2).limit_denominator(10**6)
    if abs(float(r2_frac) - best_r2) <= 1e-12 * max(1.0, abs(best_r2)):
        return r2_frac.numerator + r2_frac.denominator
    else:
        # As a fallback, still return p+q of the best rational approximation with capped denominator
        return r2_frac.numerator + r2_frac.denominator

solve(23)

# 调用 solve
result = solve(inputs['volume'])
print(result)