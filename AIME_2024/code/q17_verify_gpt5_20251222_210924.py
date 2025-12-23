inputs = {'surface_area': 54}

def solve(surface_area):
    from fractions import Fraction
    import math

    S = Fraction(surface_area, 1)  # surface area
    V = Fraction(23, 1)            # fixed volume

    # At the extremum for symmetric constraints, two sides are equal: let (x, x, y).
    # Constraints: x^2 + 2xy = S/2 and x^2 y = V => y = V/x^2.
    # Substitute into surface constraint: x^2 + 2V/x = S/2 => x^3 - (S/2)x + 2V = 0.

    # Try to find rational positive roots of 2x^3 - S x + 4V = 0 via Rational Root Theorem (when S,V integers)
    def integer_divisors(n):
        n = abs(n)
        divs = set()
        for d in range(1, int(math.isqrt(n)) + 1):
            if n % d == 0:
                divs.add(d)
                divs.add(n // d)
        return sorted(divs)

    roots_frac = []
    A, B, C, D = 2, 0, -S, 4 * V  # 2x^3 - S x + 4V = 0
    if all(z.denominator == 1 for z in (S, V)):
        Ai = int(A)
        Di = int(D)
        # candidates: p | D, q | A
        num_divs = integer_divisors(Di)
        den_divs = integer_divisors(Ai)
        seen = set()
        for pnum in num_divs:
            for qden in den_divs:
                for sgn in (1, -1):
                    x = Fraction(sgn * pnum, qden)
                    if x in seen:
                        continue
                    seen.add(x)
                    if A * x**3 + C * x + D == 0 and x > 0:
                        roots_frac.append(x)

    # Cardano for depressed cubic x^3 + p x + q = 0 with p = -S/2, q = 2V
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
        # clamp argument of acos to [-1,1] for numerical safety
        arg = (-qf / 2.0) / math.sqrt((-pf / 3.0) ** 3)
        arg = max(-1.0, min(1.0, arg))
        phi = math.acos(arg)
        roots_real = [R * math.cos((phi + 2 * k * math.pi) / 3.0) for k in range(3)]

    # Merge positive roots, avoid duplicates with fractional ones
    candidates = []
    for x in roots_frac:
        candidates.append(("frac", x))
    for xr in roots_real:
        if xr > 0:
            if not any(abs(float(xf) - xr) < 1e-12 for tag, xf in candidates if tag == "frac"):
                candidates.append(("float", xr))

    # Evaluate D^2 = a^2 + b^2 + c^2 = 2x^2 + y^2, with y = V/x^2; r^2 = D^2/4
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

    # Return p+q for r^2 = p/q in lowest terms
    if best_kind == "frac":
        r2 = best_D2_frac / 4
        r2 = r2.limit_denominator()
        return r2.numerator + r2.denominator
    else:
        # Approximate rational if no exact Fraction candidate won (shouldn't happen for this input)
        from fractions import Fraction as Fr
        r2_approx = best_D2_val / 4.0
        r2_frac = Fr(r2_approx).limit_denominator(10**9)
        return r2_frac.numerator + r2_frac.denominator

surface_area = 54
solve(surface_area)

# 调用 solve
result = solve(inputs['surface_area'])
print(result)