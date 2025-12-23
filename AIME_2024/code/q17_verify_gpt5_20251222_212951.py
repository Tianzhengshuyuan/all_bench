inputs = {'surface_area': 54}

from fractions import Fraction
import math

def solve(surface_area):
    V = Fraction(23, 1)
    S2 = Fraction(surface_area, 1) / 2  # ab + bc + ca

    # Build integer-coefficient cubic for a: a^3 - S2*a + 2V = 0
    # Clear denominators: (denS2*denV) a^3 - (numS2*denV) a + 2*(denS2*numV) = 0
    a_num, a_den = S2.numerator, S2.denominator
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

    # Try rational roots for A a^3 + C a + D = 0
    rational_roots = set()
    for p in divisors(D):
        for q in divisors(A):
            for sgn in (1, -1):
                a = Fraction(sgn * p, q)
                if a > 0 and A * a**3 + C * a + D == 0:
                    rational_roots.add(a)

    def r2_from_a(a):
        b = V / (a * a)
        D2 = b * b + 2 * a * a
        return D2 / 4

    r2_best_frac = None
    if rational_roots:
        for a in rational_roots:
            r2 = r2_from_a(a)
            if r2_best_frac is None or r2 > r2_best_frac:
                r2_best_frac = r2

    # Numeric fallback using depressed cubic x^3 + p x + q = 0 with p=-S2, q=2V
    def cbrt(x):
        return math.copysign(abs(x) ** (1.0 / 3.0), x)

    p = -float(S2)
    q = 2.0 * float(V)
    Delta = (q / 2.0) ** 2 + (p / 3.0) ** 3
    roots = []
    eps = 1e-15
    if Delta > eps:
        u = cbrt(-q / 2.0 + math.sqrt(Delta))
        v = cbrt(-q / 2.0 - math.sqrt(Delta))
        roots = [u + v]
    elif abs(Delta) <= eps:
        u = cbrt(-q / 2.0)
        roots = [2.0 * u, -u, -u]
    else:
        R = 2.0 * math.sqrt(-p / 3.0)
        arg = (-q / 2.0) / math.sqrt((-p / 3.0) ** 3)
        arg = max(-1.0, min(1.0, arg))
        phi = math.acos(arg)
        roots = [R * math.cos((phi + 2.0 * math.pi * k) / 3.0) for k in range(3)]

    r2_best_num = None
    for a_val in roots:
        if a_val > 0:
            b_val = float(V) / (a_val * a_val)
            r2_val = (b_val * b_val + 2.0 * a_val * a_val) / 4.0
            if r2_best_num is None or r2_val > r2_best_num:
                r2_best_num = r2_val

    if r2_best_frac is not None:
        r2_final = r2_best_frac.limit_denominator()
    else:
        r2_final = Fraction(r2_best_num).limit_denominator(10**12)

    return r2_final.numerator + r2_final.denominator

solve(54)

# 调用 solve
result = solve(inputs['surface_area'])
print(result)