inputs = {'surface_area': 54}

from fractions import Fraction
import math

def solve(surface_area):
    # Fixed volume
    V = Fraction(23, 1)

    # Use Fraction for exact arithmetic; limit denominator for non-integer inputs
    if isinstance(surface_area, int):
        S = Fraction(surface_area, 1)
    else:
        S = Fraction(surface_area).limit_denominator(10**12)

    sigma2 = S / 2  # ab + bc + ca

    # At extremum, two sides are equal: let sides be (x, x, y) with y = V/x^2
    # Cubic for x: x^3 - sigma2*x + 2V = 0
    # Clear denominators to use Rational Root Theorem: A x^3 + C x + D = 0
    a_num, a_den = sigma2.numerator, sigma2.denominator
    v_num, v_den = V.numerator, V.denominator
    A = a_den * v_den
    C = -a_num * v_den
    D = 2 * a_den * v_num

    def divisors(n):
        n = abs(int(n))
        res = set()
        i = 1
        while i * i <= n:
            if n % i == 0:
                res.add(i)
                res.add(n // i)
            i += 1
        return sorted(res)

    # Try rational roots via RRT on A x^3 + C x + D = 0
    rational_roots = set()
    if A != 0:
        for p in divisors(D):
            for q in divisors(A):
                for sgn in (1, -1):
                    x = Fraction(sgn * p, q)
                    if x > 0 and A * x**3 + C * x + D == 0:
                        rational_roots.add(x)

    # Compute r^2 from a candidate x: r^2 = (2x^2 + (V/x^2)^2)/4
    def r2_from_x_frac(x):
        x2 = x * x
        y2 = (V * V) / (x2 * x2)
        return (2 * x2 + y2) / 4

    best_r2_frac = None
    for x in rational_roots:
        r2 = r2_from_x_frac(x)
        if best_r2_frac is None or r2 > best_r2_frac:
            best_r2_frac = r2

    # Also solve cubic numerically to catch irrational roots
    def cbrt_real(z):
        return math.copysign(abs(z) ** (1.0 / 3.0), z)

    p_dep = -float(sigma2)
    q_dep = 2.0 * float(V)
    Delta = (q_dep / 2.0) ** 2 + (p_dep / 3.0) ** 3

    roots = []
    eps = 1e-15
    if Delta > eps:
        u = cbrt_real(-q_dep / 2.0 + math.sqrt(Delta))
        v = cbrt_real(-q_dep / 2.0 - math.sqrt(Delta))
        roots = [u + v]
    elif abs(Delta) <= eps:
        u = cbrt_real(-q_dep / 2.0)
        roots = [2.0 * u, -u, -u]
    else:
        R = 2.0 * math.sqrt(-p_dep / 3.0)
        arg = (-q_dep / 2.0) / math.sqrt((-p_dep / 3.0) ** 3)
        arg = max(-1.0, min(1.0, arg))
        phi = math.acos(arg)
        roots = [R * math.cos((phi + 2.0 * math.pi * k) / 3.0) for k in range(3)]

    best_r2_num = None
    for x in roots:
        if x > 0:
            y = float(V) / (x * x)
            r2 = 0.25 * (2.0 * x * x + y * y)
            if best_r2_num is None or r2 > best_r2_num:
                best_r2_num = r2

    # Prefer exact rational result if available; otherwise rationalize numeric best
    if best_r2_frac is not None:
        r2_final = best_r2_frac.limit_denominator()
    else:
        r2_final = Fraction(best_r2_num).limit_denominator(10**12)

    return r2_final.numerator + r2_final.denominator

surface_area = 54
solve(surface_area)

# 调用 solve
result = solve(inputs['surface_area'])
print(result)