inputs = {'volume': 23}

from fractions import Fraction
import math

def solve(volume):
    K = 27  # ab + bc + ca = 27 (surface area 54)

    # Convert volume to Fraction safely
    try:
        V = Fraction(volume)
    except:
        V = Fraction(float(volume)).limit_denominator(10**9)

    if V <= 0:
        return None

    # Try exact rational roots for x^3 - K x + 2V = 0
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

    def r2_from_x(x):
        if x <= 0:
            return None
        y = V / (x * x)
        if y <= 0:
            return None
        return (2 * x * x + y * y) / 4

    best_exact = None
    a, b = V.numerator, V.denominator
    Ps = divisors(2 * a if a != 0 else 1)
    Qs = divisors(b if b != 0 else 1)
    seen = set()
    for p in Ps:
        for q in Qs:
            for sgn in (1, -1):
                x = Fraction(sgn * p, q)
                if x <= 0 or x in seen:
                    continue
                seen.add(x)
                if b * x**3 - K * b * x + 2 * a == 0:
                    r2 = r2_from_x(x)
                    if r2 is not None and (best_exact is None or r2 > best_exact):
                        best_exact = r2

    if best_exact is not None:
        r2 = best_exact.limit_denominator()
        return r2.numerator + r2.denominator

    # Numeric fallback via Cardano/trigonometric solution
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
        r = 2.0 * math.sqrt(-p / 3.0)  # here r = 6
        phi = math.acos(max(-1.0, min(1.0, -q / (2.0 * (math.sqrt((-p / 3.0) ** 3))))))  # acos(-V/27)
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

    r2_frac = Fraction(best_r2).limit_denominator(10**6)
    return r2_frac.numerator + r2_frac.denominator

solve(23)

# 调用 solve
result = solve(inputs['volume'])
print(result)