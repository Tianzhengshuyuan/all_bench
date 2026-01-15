inputs = {'volume': 23}

from fractions import Fraction
from math import acos, cos, pi

def solve(volume):
    K = 27  # ab + bc + ca = 27 (since surface area is 54)

    # Convert volume to Fraction safely
    try:
        V = Fraction(volume)
    except:
        V = Fraction(float(volume)).limit_denominator(10**9)

    # Feasible range: 0 < V <= 27 (achieved at a=b=c=3)
    if V <= 0 or V > 27:
        return None

    # Try exact rational roots first: solve b*x^3 - K*b*x + 2*a = 0 where V = a/b
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
        return ds or {1}

    a, b = V.numerator, V.denominator
    best_exact = None
    if a != 0:
        Ps = divisors(2 * a)
        Qs = divisors(b if b != 0 else 1)
        seen = set()
        for p in Ps:
            for q in Qs:
                for sgn in (1, -1):
                    x = Fraction(sgn * p, q)
                    if x <= 0 or x in seen:
                        continue
                    seen.add(x)
                    # Check exact root
                    if b * x**3 - K * b * x + 2 * a == 0:
                        y = V / (x * x)
                        if y > 0:
                            r2 = (2 * x * x + y * y) / 4
                            if best_exact is None or r2 > best_exact:
                                best_exact = r2
    if best_exact is not None:
        r2 = best_exact.limit_denominator()
        return r2.numerator + r2.denominator

    # Numeric fallback via trigonometric solution (for 0 < V <= 27)
    V_float = float(V)
    arg = max(-1.0, min(1.0, -V_float / 27.0))
    theta = acos(arg)  # phi
    best_r2 = None
    for k in (0, 1, 2):
        x = 6.0 * cos((theta + 2 * pi * k) / 3.0)
        if x > 1e-15:
            y = V_float / (x * x)
            if y > 0:
                r2 = (2.0 * x * x + y * y) / 4.0
                if best_r2 is None or r2 > best_r2:
                    best_r2 = r2

    if best_r2 is None:
        return None

    r2_frac = Fraction(best_r2).limit_denominator(10**9)
    return r2_frac.numerator + r2_frac.denominator

solve(23)

# 调用 solve
result = solve(inputs['volume'])
print(result)