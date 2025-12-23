inputs = {'surface_area': 54}

def solve(surface_area):
    from fractions import Fraction
    import math

    V = Fraction(23, 1)
    S = Fraction(surface_area, 1)
    sigma2 = S / 2  # ab + bc + ca

    # Construct integer-coefficient cubic: A x^3 + C x + D = 0
    a, b = sigma2.numerator, sigma2.denominator
    n, d = V.numerator, V.denominator
    A = b * d
    C = -a * d
    D = 2 * b * n

    def divisors(N):
        N = abs(int(N))
        res = set()
        i = 1
        while i * i <= N:
            if N % i == 0:
                res.add(i)
                res.add(N // i)
            i += 1
        return sorted(res)

    # Try rational roots via Rational Root Theorem
    rational_roots = set()
    for p in divisors(D):
        for q in divisors(A):
            if q == 0:
                continue
            for sgn in (1, -1):
                x = Fraction(sgn * p, q)
                if x > 0 and A * x**3 + C * x + D == 0:
                    rational_roots.add(x)

    # Evaluate r^2 = (2x^2 + y^2)/4 with y = V/x^2 for rational roots
    r2_frac_best = None
    for x in rational_roots:
        y = V / (x * x)
        r2 = Fraction(1, 4) * (2 * x * x + y * y)
        if r2_frac_best is None or r2 > r2_frac_best:
            r2_frac_best = r2

    # Solve cubic numerically for completeness: x^3 - sigma2 x + 2V = 0
    p_dep = -float(sigma2)
    q_dep = 2.0 * float(V)
    Delta = (q_dep / 2.0) ** 2 + (p_dep / 3.0) ** 3

    def cbrt_real(x):
        return math.copysign(abs(x) ** (1.0 / 3.0), x)

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
        denom = math.sqrt((-p_dep / 3.0) ** 3)
        val = (-q_dep / 2.0) / denom
        val = max(-1.0, min(1.0, val))
        phi = math.acos(val)
        roots = [R * math.cos((phi + 2.0 * math.pi * k) / 3.0) for k in range(3)]

    r2_num_best = None
    for x in roots:
        if x > 0:
            y = float(V) / (x * x)
            r2 = 0.25 * (2.0 * x * x + y * y)
            if r2_num_best is None or r2 > r2_num_best:
                r2_num_best = r2

    # Prefer exact if it matches the numerical maximum; otherwise approximate
    if r2_frac_best is not None and r2_num_best is not None and abs(float(r2_frac_best) - r2_num_best) <= 1e-12 * (1 + abs(r2_num_best)):
        r2_final = r2_frac_best
    else:
        if r2_num_best is None:
            if r2_frac_best is None:
                return None
            r2_final = r2_frac_best
        else:
            r2_final = Fraction(r2_num_best).limit_denominator(10**9)

    return r2_final.numerator + r2_final.denominator

surface_area = 54
solve(surface_area)

# 调用 solve
result = solve(inputs['surface_area'])
print(result)