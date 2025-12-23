inputs = {'surface_area': 54}

def solve(surface_area):
    from fractions import Fraction
    from math import sqrt, acos, cos, pi, isclose

    V = Fraction(23, 1)
    S = Fraction(surface_area, 1)
    sigma2 = S / 2  # ab + bc + ca

    # Build integer-coefficient polynomial A x^3 + C x + D = 0
    # from x^3 - sigma2*x + 2V = 0 by clearing denominators
    a = sigma2.numerator
    b = sigma2.denominator
    n = V.numerator
    d = V.denominator

    def gcd(u, v):
        while v:
            u, v = v, u % v
        return abs(u)

    def lcm(u, v):
        return abs(u // gcd(u, v) * v)

    L = lcm(b, d)
    A = L
    C = -a * (L // b)
    D = 2 * n * (L // d)

    def divisors(N):
        N = abs(int(N))
        if N == 0:
            return {0}
        res = set()
        i = 1
        while i * i <= N:
            if N % i == 0:
                res.add(i)
                res.add(N // i)
            i += 1
        return sorted(res)

    # Try rational roots via RRT on A x^3 + C x + D = 0
    rational_roots = set()
    for p in divisors(D):
        for q in divisors(A):
            if q == 0:
                continue
            for sgn in (1, -1):
                x = Fraction(sgn * p, q)
                if x > 0 and A * x**3 + C * x + D == 0:
                    rational_roots.add(x)

    # Evaluate r^2 = (2x^2 + y^2)/4 with y = V/x^2 for rational roots, take maximum
    r2_frac_best = None
    if rational_roots:
        for x in rational_roots:
            y = V / (x * x)
            r2 = Fraction(1, 4) * (2 * x * x + y * y)
            if r2_frac_best is None or r2 > r2_frac_best:
                r2_frac_best = r2

    # Solve cubic numerically (Cardano/trigonometric) for completeness
    p_dep = -float(sigma2)
    q_dep = 2.0 * float(V)
    Delta = (q_dep / 2.0) ** 2 + (p_dep / 3.0) ** 3

    def cbrt_real(x):
        return (abs(x) ** (1.0 / 3.0)) * (1 if x >= 0 else -1)

    roots = []
    if Delta >= -1e-15:
        sqrtD = sqrt(Delta) if Delta > 0 else 0.0
        u = cbrt_real(-q_dep / 2.0 + sqrtD)
        v = cbrt_real(-q_dep / 2.0 - sqrtD)
        roots = [u + v]
    else:
        R = 2.0 * sqrt(-p_dep / 3.0)
        denom = sqrt((-p_dep / 3.0) ** 3)
        val = (-q_dep / 2.0) / denom
        val = max(-1.0, min(1.0, val))
        phi = acos(val)
        roots = [R * cos((phi + 2.0 * pi * k) / 3.0) for k in range(3)]

    r2_num_best = None
    for x in roots:
        if x > 0:
            y = float(V) / (x * x)
            r2 = 0.25 * (2.0 * x * x + y * y)
            if r2_num_best is None or r2 > r2_num_best:
                r2_num_best = r2

    # Prefer exact if it matches the numerical maximum
    if r2_frac_best is not None and r2_num_best is not None and isclose(float(r2_frac_best), r2_num_best, rel_tol=1e-12, abs_tol=1e-12):
        r2_final = r2_frac_best
    else:
        if r2_num_best is None:
            return None
        r2_final = Fraction(r2_num_best).limit_denominator(10**9)

    return r2_final.numerator + r2_final.denominator

solve(54)

# 调用 solve
result = solve(inputs['surface_area'])
print(result)