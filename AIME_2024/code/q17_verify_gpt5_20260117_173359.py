inputs = {'surface_area': 54}

def solve(surface_area):
    from fractions import Fraction
    import math

    V = 23  # fixed volume from the problem
    S = Fraction(surface_area)
    s2 = S / 2  # xy + yz + zx

    # Find positive rational roots of a^3 - s2*a + 2V = 0 using Rational Root Theorem
    den = s2.denominator
    num_s2 = s2.numerator
    A = den
    C = 2 * V * den

    def divisors(n):
        n = abs(int(n))
        if n == 0:
            return {0}
        res = set()
        i = 1
        while i * i <= n:
            if n % i == 0:
                res.add(i)
                res.add(n // i)
            i += 1
        return res

    rational_as = set()
    for p in divisors(C):
        for q in divisors(A):
            if q == 0:
                continue
            for sign in (1, -1):
                a = Fraction(sign * p, q)
                if a > 0 and (a**3 - s2 * a + 2 * V) == 0:
                    rational_as.add(a)

    # Compute diag^2 and r^2 for candidates
    def diag2_from_a_frac(a):
        return 2 * a * a + Fraction(V * V, 1) / (a * a * a * a)

    best_diag2_float = -1.0
    best_r2_frac = None

    for a in rational_as:
        d2 = diag2_from_a_frac(a)
        d2f = float(d2)
        if d2f > best_diag2_float:
            best_diag2_float = d2f
            best_r2_frac = d2 / 4

    # Also consider irrational roots via Cardano to ensure global maximum
    # Depressed cubic: t^3 + p t + q = 0 with p = -s2, q = 2V
    p = -float(s2)
    q = 2.0 * V

    def cbrt(x):
        return math.copysign(abs(x) ** (1.0 / 3.0), x)

    def real_roots_depressed(pv, qv):
        D = (qv / 2.0) ** 2 + (pv / 3.0) ** 3
        roots = []
        eps = 1e-15
        if D > eps:
            A_ = -qv / 2.0 + math.sqrt(D)
            B_ = -qv / 2.0 - math.sqrt(D)
            roots = [cbrt(A_) + cbrt(B_)]
        elif D >= -eps:
            u = cbrt(-qv / 2.0)
            roots = [2.0 * u, -u, -u]
        else:
            r = math.sqrt(-pv / 3.0)
            theta = math.acos(-qv / (2.0 * r ** 3))
            roots = [2.0 * r * math.cos((theta + 2 * k * math.pi) / 3.0) for k in range(3)]
        return roots

    roots = real_roots_depressed(p, q)
    for a in roots:
        if a > 0:
            d2f = 2.0 * a * a + (V * V) / (a ** 4)
            if d2f > best_diag2_float:
                best_diag2_float = d2f
                # No exact fraction known; approximate rational r^2
                r2_approx = d2f / 4.0
                best_r2_frac = Fraction(r2_approx).limit_denominator(10**9)

    # Return p + q for r^2 = p/q in lowest terms
    r2 = best_r2_frac
    return r2.numerator + r2.denominator

solve(54)

# 调用 solve
result = solve(inputs['surface_area'])
print(result)