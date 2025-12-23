inputs = {'surface_area': 54}

from fractions import Fraction
import math

def solve(surface_area):
    # Constants
    P = Fraction(23, 1)  # volume constraint xyz = 23
    SA = Fraction(surface_area).limit_denominator(10**6)
    S2 = SA / 2  # xy + yz + zx = surface_area / 2

    # We maximize the space diagonal squared D2 = x^2 + y^2 + z^2
    # Using symmetry, at extremum two sides are equal: let y = z = a, x = b
    # Constraints give: a^2 + 2ab = S2 and a^2 b = P -> b = P / a^2
    # Substitute: a^2 + 2P/a = S2 -> a^3 - S2*a + 2P = 0
    # Solve depressed cubic for a > 0, then choose the one maximizing D2 = b^2 + 2a^2

    # Try to find rational roots first (exact arithmetic)
    def lcm(a, b):
        return abs(a * b) // math.gcd(a, b)

    a3 = Fraction(1, 1)
    a1 = -S2
    a0 = 2 * P
    den_lcm = 1
    for frac in (a3, a1, a0):
        den_lcm = lcm(den_lcm, frac.denominator)
    A = int(a3 * den_lcm)
    C = int(a1 * den_lcm)
    D = int(a0 * den_lcm)

    def positive_divisors(n):
        n = abs(n)
        res = set()
        i = 1
        while i * i <= n:
            if n % i == 0:
                res.add(i)
                res.add(n // i)
            i += 1
        return sorted(res)

    rational_roots = set()
    if A != 0:
        for p in positive_divisors(D):
            for sign in (1, -1):
                num = sign * p
                for q in positive_divisors(A):
                    r = Fraction(num, q)
                    val = r**3 + a1 * r + a0
                    if val == 0:
                        if r > 0:
                            rational_roots.add(r)

    # Compute candidate r^2 and choose maximum
    def r2_from_a(a):
        b = P / (a * a)
        D2 = b * b + 2 * a * a
        return D2 / 4

    r2_candidates_frac = []
    for a in rational_roots:
        r2_candidates_frac.append(r2_from_a(a))

    # Numeric fallback to ensure we have the maximum (handles cases without rational roots)
    def cubic_real_roots_depressed(p, q):
        # Solve x^3 + p x + q = 0
        roots = []
        def cbrt(x):
            return math.copysign(abs(x) ** (1.0 / 3.0), x)
        Δ = (q / 2.0) ** 2 + (p / 3.0) ** 3
        if Δ > 1e-14:
            sqrtΔ = math.sqrt(Δ)
            u = cbrt(-q / 2.0 + sqrtΔ)
            v = cbrt(-q / 2.0 - sqrtΔ)
            roots.append(u + v)
        elif abs(Δ) <= 1e-14:
            t = cbrt(-q / 2.0)
            roots.extend([2.0 * t, -t])
        else:
            r = math.sqrt(-p / 3.0)
            cos_arg = max(-1.0, min(1.0, -q / (2.0 * r**3)))
            phi = math.acos(cos_arg)
            for k in range(3):
                roots.append(2.0 * r * math.cos((phi + 2.0 * math.pi * k) / 3.0))
        return roots

    p_float = -float(S2)
    q_float = float(2 * P)
    roots_float = cubic_real_roots_depressed(p_float, q_float)
    r2_best_float = -float('inf')
    for a_val in roots_float:
        if a_val > 1e-12:
            b_val = float(P) / (a_val * a_val)
            D2_val = b_val * b_val + 2.0 * a_val * a_val
            r2_val = D2_val / 4.0
            if r2_val > r2_best_float:
                r2_best_float = r2_val

    # Prefer exact rational candidate if it matches the numeric maximum
    r2_best = None
    if r2_candidates_frac:
        # Choose the rational candidate with largest value
        r2_frac_best = max(r2_candidates_frac, key=lambda x: float(x))
        if r2_best_float == -float('inf') or abs(float(r2_frac_best) - r2_best_float) <= 1e-8 * max(1.0, abs(r2_best_float)):
            r2_best = r2_frac_best

    if r2_best is None:
        # Fall back to rational approximation of the numeric maximum
        r2_best = Fraction(r2_best_float).limit_denominator(10**6)

    # Return p + q where r^2 = p/q in lowest terms
    r2_best = Fraction(r2_best.numerator, r2_best.denominator)  # ensure reduced
    return r2_best.numerator + r2_best.denominator

solve(surface_area)

# 调用 solve
result = solve(inputs['surface_area'])
print(result)