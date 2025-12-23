inputs = {'surface_area': 54}

def solve(surface_area):
    from fractions import Fraction
    import math

    S = Fraction(surface_area, 1)
    V = Fraction(23, 1)

    # At extremum, two sides equal: (x, x, y), with y = V/x^2 and surface constraint:
    # x^2 + 2xy = S/2  =>  x^3 - (S/2)x + 2V = 0, i.e., t^3 + p t + q = 0 with:
    p = -S / 2
    q = 2 * V

    # Try to find rational positive roots using Rational Root Theorem
    roots_frac = []
    if q.denominator == 1:
        const = abs(q.numerator)
        divisors = set()
        for d in range(1, int(math.isqrt(const)) + 1):
            if const % d == 0:
                divisors.add(d)
                divisors.add(const // d)
        for rnum in sorted(divisors):
            for sgn in (1, -1):
                x = Fraction(sgn * rnum, 1)
                if x > 0 and x**3 + p * x + q == 0:
                    roots_frac.append(x)

    # Cardano's formula for real roots of depressed cubic t^3 + p t + q = 0
    def cbrt(x):
        return math.copysign(abs(x) ** (1.0 / 3.0), x)

    pf = float(p)
    qf = float(q)
    Delta = (qf / 2) ** 2 + (pf / 3) ** 3
    roots_real = []
    eps = 1e-14
    if Delta > eps:
        u = cbrt(-qf / 2 + math.sqrt(Delta))
        v = cbrt(-qf / 2 - math.sqrt(Delta))
        roots_real = [u + v]
    elif abs(Delta) <= eps:
        u = cbrt(-qf / 2)
        roots_real = [2 * u, -u, -u]
    else:
        R = 2 * math.sqrt(-pf / 3.0)
        phi = math.acos((-qf / 2) / math.sqrt((-pf / 3.0) ** 3))
        roots_real = [R * math.cos((phi + 2 * k * math.pi) / 3.0) for k in range(3)]

    # Merge positive roots, avoiding duplicates with fractional ones
    candidates = []
    for x in roots_frac:
        candidates.append(("frac", x))
    for xr in roots_real:
        if xr > 0:
            dup = any(abs(float(xf) - xr) < 1e-9 for (tag, xf) in candidates if tag == "frac")
            if not dup:
                candidates.append(("float", xr))

    # Evaluate D^2 = y^2 + 2x^2 where y = V/x^2, then r^2 = D^2/4
    best_kind = None
    best_D2_frac = None
    best_D2_val = -float("inf")

    for kind, xv in candidates:
        if kind == "frac":
            x = xv
            y = V / (x * x)
            D2 = y * y + 2 * (x * x)  # Fraction
            val = float(D2)
            if val > best_D2_val:
                best_D2_val = val
                best_D2_frac = D2
                best_kind = "frac"
        else:
            x = xv
            D2_val = (float(V) ** 2) / (x ** 4) + 2 * (x ** 2)
            if D2_val > best_D2_val:
                best_D2_val = D2_val
                best_D2_frac = None
                best_kind = "float"

    if best_kind == "frac":
        r2 = best_D2_frac / 4
        r2 = r2.limit_denominator()
        return r2.numerator + r2.denominator
    else:
        r2_approx = best_D2_val / 4
        r2_frac = Fraction(r2_approx).limit_denominator(10**9)
        return r2_frac.numerator + r2_frac.denominator

surface_area = 54
solve(surface_area)

# 调用 solve
result = solve(inputs['surface_area'])
print(result)