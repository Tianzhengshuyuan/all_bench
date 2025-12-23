inputs = {'surface_area': 54}

def solve(surface_area):
    from fractions import Fraction
    import math

    S = Fraction(surface_area, 1)
    V = Fraction(23, 1)

    # Lagrange multipliers imply at extremum two edges are equal: let (x, x, y).
    # Constraints: x^2 + 2xy = S/2 and x^2 y = V => y = V/x^2.
    # Substitute: x^2 + 2x(V/x^2) = S/2  =>  x^3 - (S/2)x + 2V = 0.
    # Multiply by 2 to get integer coefficients: 2x^3 - S x + 4V = 0.
    A = 2
    B = 0
    C = -S
    D = 4 * V  # all are Fractions but S,V are integers, so coefficients are integers

    # Collect rational roots via Rational Root Theorem for Ax^3 + Bx^2 + Cx + D = 0
    def integer_divisors(n):
        n = abs(n)
        divs = set()
        for d in range(1, int(math.isqrt(n)) + 1):
            if n % d == 0:
                divs.add(d)
                divs.add(n // d)
        return sorted(divs)

    roots_frac = []
    # Only attempt RRT when all coeffs are integers
    if all(isinstance(z, Fraction) and z.denominator == 1 for z in (S, V)):
        Ai = int(A)  # =2
        Ci = int(C)  # = -S
        Di = int(D)  # = 4V
        num_divs = integer_divisors(abs(Di))
        den_divs = integer_divisors(abs(Ai))
        seen = set()
        for p in num_divs:
            for q in den_divs:
                for sgn in (1, -1):
                    x = Fraction(sgn * p, q)
                    if x in seen:
                        continue
                    seen.add(x)
                    # Evaluate 2x^3 - S x + 4V exactly
                    if A * x**3 + C * x + D == 0:
                        if x > 0:
                            roots_frac.append(x)

    # Solve depressed cubic x^3 + p x + q = 0 with p = -S/2, q = 2V
    p = -S / 2
    q = 2 * V

    def cbrt_real(x):
        return math.copysign(abs(x) ** (1.0 / 3.0), x)

    pf = float(p)
    qf = float(q)
    Delta = (qf / 2.0) ** 2 + (pf / 3.0) ** 3
    roots_real = []
    eps = 1e-15
    if Delta > eps:
        u = cbrt_real(-qf / 2.0 + math.sqrt(Delta))
        v = cbrt_real(-qf / 2.0 - math.sqrt(Delta))
        roots_real = [u + v]
    elif abs(Delta) <= eps:
        u = cbrt_real(-qf / 2.0)
        roots_real = [2.0 * u, -u, -u]
    else:
        R = 2.0 * math.sqrt(-pf / 3.0)
        phi = math.acos(max(-1.0, min(1.0, (-qf / 2.0) / math.sqrt((-pf / 3.0) ** 3))))
        roots_real = [R * math.cos((phi + 2 * k * math.pi) / 3.0) for k in range(3)]

    # Merge candidates (positive roots only)
    candidates = []
    for x in roots_frac:
        candidates.append(("frac", x))
    for xr in roots_real:
        if xr > 0:
            # avoid duplicates with fractional ones
            dup = any(abs(float(xf) - xr) < 1e-12 for tag, xf in candidates if tag == "frac")
            if not dup:
                candidates.append(("float", xr))

    # Evaluate D^2 = a^2 + b^2 + c^2 = 2x^2 + y^2, with y = V/x^2
    best_kind = None
    best_D2_frac = None
    best_D2_val = -float("inf")

    for kind, xv in candidates:
        if kind == "frac":
            x = xv
            y = V / (x * x)
            D2 = 2 * (x * x) + (y * y)  # exact Fraction
            val = float(D2)
            if val > best_D2_val:
                best_D2_val = val
                best_D2_frac = D2
                best_kind = "frac"
        else:
            x = xv
            y = float(V) / (x * x)
            D2_val = 2.0 * (x * x) + (y * y)
            if D2_val > best_D2_val:
                best_D2_val = D2_val
                best_D2_frac = None
                best_kind = "float"

    # r^2 = D^2 / 4; return p+q for r^2 = p/q in lowest terms
    if best_kind == "frac":
        r2 = (best_D2_frac) / 4
        r2 = r2.limit_denominator()
        return r2.numerator + r2.denominator
    else:
        from fractions import Fraction as Fr
        r2_approx = best_D2_val / 4.0
        r2_frac = Fr(r2_approx).limit_denominator(10**9)
        return r2_frac.numerator + r2_frac.denominator

surface_area = 54
solve(surface_area)

# 调用 solve
result = solve(inputs['surface_area'])
print(result)