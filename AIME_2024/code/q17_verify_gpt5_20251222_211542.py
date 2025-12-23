inputs = {'surface_area': 54}

def solve(surface_area):
    from fractions import Fraction
    import math

    S = Fraction(surface_area, 1)  # surface area
    V = Fraction(23, 1)            # fixed volume

    # Extremum occurs when two sides are equal: let (x, x, y).
    # Constraints: x^2 + 2xy = S/2 and x^2 y = V => y = V/x^2.
    # Substitute into surface constraint: x^2 + 2V/x = S/2 => x^3 - (S/2)x + 2V = 0
    # Equivalently: 2x^3 - S x + 4V = 0

    # Try rational roots first (Rational Root Theorem) for exact arithmetic
    roots_frac = []
    A, C, D = Fraction(2, 1), -S, 4 * V  # 2x^3 - S x + 4V = 0
    if S.denominator == 1 and V.denominator == 1:
        def integer_divisors(n):
            n = abs(n)
            divs = set()
            for d in range(1, int(math.isqrt(n)) + 1):
                if n % d == 0:
                    divs.add(d)
                    divs.add(n // d)
            return sorted(divs)

        Ai = int(A)
        Di = int(D)
        den_divs = integer_divisors(abs(Ai))
        num_divs = integer_divisors(abs(Di))
        seen = set()
        for p in num_divs:
            for q in den_divs:
                for sgn in (1, -1):
                    x = Fraction(sgn * p, q)
                    if x in seen:
                        continue
                    seen.add(x)
                    if A * x**3 + C * x + D == 0 and x > 0:
                        roots_frac.append(x)

    # If rational roots found, compute r^2 exactly and take the maximum
    best_r2_frac = None
    if roots_frac:
        for x in roots_frac:
            y = V / (x * x)
            r2 = (2 * x * x + y * y) / 4  # exact Fraction
            if best_r2_frac is None or r2 > best_r2_frac:
                best_r2_frac = r2

    # If no exact rational root or to be safe, solve cubic numerically for all real roots
    def cbrt_real(x):
        return math.copysign(abs(x) ** (1.0 / 3.0), x)

    p_dep = -float(S) / 2.0
    q_dep = 2.0 * float(V)
    Delta = (q_dep / 2.0) ** 2 + (p_dep / 3.0) ** 3

    roots_real = []
    eps = 1e-15
    if Delta > eps:
        u = cbrt_real(-q_dep / 2.0 + math.sqrt(Delta))
        v = cbrt_real(-q_dep / 2.0 - math.sqrt(Delta))
        roots_real = [u + v]
    elif abs(Delta) <= eps:
        u = cbrt_real(-q_dep / 2.0)
        roots_real = [2.0 * u, -u, -u]
    else:
        R = 2.0 * math.sqrt(-p_dep / 3.0)
        arg = (-q_dep / 2.0) / math.sqrt((-p_dep / 3.0) ** 3)
        arg = max(-1.0, min(1.0, arg))
        phi = math.acos(arg)
        roots_real = [R * math.cos((phi + 2 * k * math.pi) / 3.0) for k in range(3)]

    best_r2_num = None
    for x in roots_real:
        if x > 0:
            y = float(V) / (x * x)
            r2 = (2.0 * x * x + y * y) / 4.0
            if best_r2_num is None or r2 > best_r2_num:
                best_r2_num = r2

    # Prefer exact if available; otherwise approximate as a rational
    if best_r2_frac is not None:
        r2_final = best_r2_frac
    else:
        from fractions import Fraction as Fr
        r2_final = Fr(best_r2_num).limit_denominator(10**9)

    return r2_final.numerator + r2_final.denominator

solve(surface_area)

# 调用 solve
result = solve(inputs['surface_area'])
print(result)