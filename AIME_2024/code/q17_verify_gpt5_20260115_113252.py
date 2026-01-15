inputs = {'surface_area': 54}

def solve(surface_area):
    import math
    from fractions import Fraction

    V = 23.0  # fixed volume in the problem

    def cbrt(x):
        return math.copysign(abs(x) ** (1/3), x)

    # Solve depressed cubic: a^3 + p a + q = 0
    def depressed_cubic_real_roots(p, q):
        roots = []
        Δ = (q/2.0)**2 + (p/3.0)**3
        eps = 1e-14
        if Δ >= -eps:
            sqrtΔ = math.sqrt(max(0.0, Δ))
            u = cbrt(-q/2.0 + sqrtΔ)
            v = cbrt(-q/2.0 - sqrtΔ)
            roots.append(u + v)
        else:
            A = 2.0 * math.sqrt(-p / 3.0)
            arg = (3.0 * q) / (2.0 * p) * math.sqrt(-3.0 / p)
            arg = max(-1.0, min(1.0, arg))
            theta = math.acos(arg)
            for k in range(3):
                roots.append(A * math.cos((theta - 2.0 * math.pi * k) / 3.0))
        return roots

    S = float(surface_area)
    p = -S / 2.0
    q = 2.0 * V

    roots = depressed_cubic_real_roots(p, q)
    pos_roots = [a for a in roots if a > 1e-12]

    if not pos_roots:
        return None

    best_r2 = -1.0
    for a in pos_roots:
        b = V / (a * a)
        D2 = 2.0 * a * a + b * b
        r2 = D2 / 4.0
        if r2 > best_r2:
            best_r2 = r2

    frac = Fraction(best_r2).limit_denominator(10**9)
    return frac.numerator + frac.denominator

solve(54)

# 调用 solve
result = solve(inputs['surface_area'])
print(result)