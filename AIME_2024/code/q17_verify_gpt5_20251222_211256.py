inputs = {'surface_area': 54}

def solve(surface_area):
    from fractions import Fraction
    from math import sqrt, acos, cos, pi, isclose

    V = Fraction(23, 1)

    def divisors(n):
        n = abs(int(n))
        divs = set()
        i = 1
        while i * i <= n:
            if n % i == 0:
                divs.add(i)
                divs.add(n // i)
            i += 1
        return sorted(divs)

    SA = Fraction(surface_area, 1)
    sigma2 = SA / 2  # ab+bc+ca

    # Try to find rational positive roots of x^3 - sigma2*x + 2V = 0
    A = sigma2.numerator
    B = sigma2.denominator
    N = 2 * V.numerator * B // V.denominator  # constant term after clearing denominators is 2VB
    cand_ps = divisors(N)
    cand_qs = divisors(B)

    rational_roots = set()
    for p in cand_ps:
        for q in cand_qs:
            for sgn in (1, -1):
                x = Fraction(sgn * p, q)
                # Evaluate B*x^3 - A*x + 2*V*B == 0
                if B * x**3 - A * x + 2 * V * B == 0:
                    if x > 0:
                        rational_roots.add(x)

    r2_rat = None
    if rational_roots:
        best = None
        for x in rational_roots:
            y = V / (x * x)
            s1 = 2 * x + y
            r2 = Fraction(1, 4) * (s1 * s1 - 2 * sigma2)
            if best is None or r2 > best:
                best = r2
        r2_rat = best

    # Numeric roots of depressed cubic x^3 + p x + q = 0 with p=-sigma2, q=2V
    p = -float(sigma2)
    q = 2.0 * float(V)
    Delta = (q / 2.0) ** 2 + (p / 3.0) ** 3

    def cbrt(x):
        return (abs(x) ** (1.0 / 3.0)) * (1 if x >= 0 else -1)

    roots = []
    if Delta >= -1e-15:
        sqrtD = sqrt(Delta) if Delta > 0 else 0.0
        u = cbrt(-q / 2.0 + sqrtD)
        v = cbrt(-q / 2.0 - sqrtD)
        roots = [u + v]
    else:
        r = 2.0 * sqrt(-p / 3.0)
        denom = sqrt(-((p / 3.0) ** 3))
        val = (-q / 2.0) / denom
        if val < -1.0:
            val = -1.0
        elif val > 1.0:
            val = 1.0
        phi = acos(val)
        roots = [r * cos((phi + 2.0 * pi * k) / 3.0) for k in range(3)]

    # Evaluate r^2 numerically for positive roots and take maximum
    r2_numeric = None
    for x in roots:
        if x > 0:
            y = float(V) / (x * x)
            s1 = 2.0 * x + y
            r2 = 0.25 * (s1 * s1 - 2.0 * float(sigma2))
            if r2_numeric is None or r2 > r2_numeric:
                r2_numeric = r2

    # Prefer exact rational if it matches the numerical maximum
    if r2_rat is not None and r2_numeric is not None and isclose(float(r2_rat), r2_numeric, rel_tol=1e-12, abs_tol=1e-12):
        r2_final = r2_rat
    else:
        # Fallback to rational approximation if needed
        if r2_numeric is None:
            return None
        r2_final = Fraction(r2_numeric).limit_denominator(10**9)

    return r2_final.numerator + r2_final.denominator

solve(54)

# 调用 solve
result = solve(inputs['surface_area'])
print(result)