inputs = {'volume': 23}

from fractions import Fraction
import math

def solve(volume):
    S = 27  # ab+bc+ca = 27 since surface area is 54
    V = Fraction(volume).limit_denominator()

    def divisors(n):
        n = abs(n)
        ds = set()
        for i in range(1, int(n**0.5) + 1):
            if n % i == 0:
                ds.add(i)
                ds.add(n // i)
        return sorted(ds)

    def r2_from_x_frac(x_frac):
        if x_frac <= 0:
            return None
        y = V / (x_frac * x_frac)
        if y <= 0:
            return None
        r2 = (y * y + 2 * x_frac * x_frac) / 4
        return r2

    # Try to find rational positive roots first (exact)
    roots_frac = set()
    a = V.numerator
    b = V.denominator
    # Polynomial with integer coefficients: b*x^3 - S*b*x + 2*a = 0
    num_divs = divisors(2 * a if a != 0 else 1)
    den_divs = divisors(b if b != 0 else 1)
    for p in num_divs:
        for q in den_divs:
            for sgn in (1, -1):
                r = Fraction(sgn * p, q)
                # exact evaluation
                val = b * r**3 - S * b * r + 2 * a
                if val == 0 and r > 0:
                    roots_frac.add(r)

    best_r2_frac = None
    if roots_frac:
        for x in roots_frac:
            r2 = r2_from_x_frac(x)
            if r2 is not None:
                if best_r2_frac is None or r2 > best_r2_frac:
                    best_r2_frac = r2
        if best_r2_frac is not None:
            best_r2_frac = best_r2_frac.limit_denominator()
            return best_r2_frac.numerator + best_r2_frac.denominator

    # If no rational roots, fall back to numeric Cardano to handle general volume
    p = -S
    q = 2 * float(V)
    disc = (q / 2.0) ** 2 + (p / 3.0) ** 3

    def cbrt(x):
        return math.copysign(abs(x) ** (1.0 / 3.0), x)

    roots = []
    if disc > 0:
        sqrt_disc = math.sqrt(disc)
        u = cbrt(-q / 2.0 + sqrt_disc)
        v = cbrt(-q / 2.0 - sqrt_disc)
        roots = [u + v]
    elif abs(disc) < 1e-18:
        if abs(q) < 1e-18:
            roots = [0.0, 0.0, 0.0]
        else:
            u = cbrt(-q / 2.0)
            roots = [2 * u, -u, -u]
    else:
        r = 2.0 * math.sqrt(-p / 3.0)
        phi = math.acos((-q / 2.0) / math.sqrt((-p / 3.0) ** 3))
        roots = [r * math.cos((phi + 2 * math.pi * k) / 3.0) for k in range(3)]

    best_r2 = None
    for x in roots:
        if x > 1e-12:
            y = float(V) / (x * x)
            if y > 0:
                r2 = (y * y + 2 * x * x) / 4.0
                if best_r2 is None or r2 > best_r2:
                    best_r2 = r2

    if best_r2 is not None:
        # Try to detect rational result
        frac_approx = Fraction(best_r2).limit_denominator(10**9)
        if abs(best_r2 - float(frac_approx)) < 1e-12:
            return frac_approx.numerator + frac_approx.denominator
        return best_r2
    return None

solve(volume)

# 调用 solve
result = solve(inputs['volume'])
print(result)