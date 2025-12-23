inputs = {'surface_area': 54}

from fractions import Fraction
import math

def solve(surface_area):
    S = Fraction(surface_area, 1)
    V = Fraction(23, 1)
    sigma2 = S / 2  # ab + bc + ca

    # Cubic for extremal box with two equal edges: x^3 - sigma2*x + 2V = 0
    # Clear denominators: A x^3 + C x + D = 0 with integer coefficients
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
    for pnum in divisors(D):
        for qden in divisors(A):
            for sgn in (1, -1):
                x = Fraction(sgn * pnum, qden)
                if x > 0 and A * x**3 + C * x + D == 0:
                    rational_roots.add(x)

    # Evaluate candidates; track best r^2 value and exact fraction if available
    best_val = -float("inf")
    best_frac = None

    # From a root x (with sides x, x, y where y = V/x^2), the space diagonal squared is D2 = 2x^2 + y^2
    # Then r^2 = D2 / 4
    for x in rational_roots:
        y = V / (x * x)
        D2 = 2 * (x * x) + (y * y)  # Fraction
        r2 = D2 / 4
        val = float(r2)
        if val > best_val:
            best_val = val
            best_frac = r2

    # Solve cubic numerically for completeness to catch irrational roots
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

    for xr in roots:
        if xr > 0:
            y = float(V) / (xr * xr)
            r2_val = 0.25 * (2.0 * xr * xr + y * y)
            if r2_val > best_val + 1e-12:
                best_val = r2_val
                best_frac = None  # best is irrational (or we didn't find exact form)

    # Return p+q for r^2 = p/q in lowest terms
    if best_frac is not None:
        r2_final = best_frac.limit_denominator()
    else:
        r2_final = Fraction(best_val).limit_denominator(10**12)

    return r2_final.numerator + r2_final.denominator

surface_area = 54
solve(surface_area)

# 调用 solve
result = solve(inputs['surface_area'])
print(result)