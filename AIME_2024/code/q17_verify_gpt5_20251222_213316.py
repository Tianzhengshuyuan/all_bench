inputs = {'surface_area': 54}

from fractions import Fraction
import math

def solve(surface_area):
    V = 23  # fixed volume from the problem
    S = surface_area

    # Try to find an exact rational positive root among divisors of 2V (Rational Root Theorem)
    x_exact = None
    if isinstance(S, int) or (isinstance(S, float) and abs(S - round(S)) < 1e-12):
        S_int = int(round(S))
        S_frac = Fraction(S_int, 1)
        def divisors(n):
            res = set()
            for d in range(1, int(math.isqrt(n)) + 1):
                if n % d == 0:
                    res.add(d)
                    res.add(n // d)
            return sorted(res)
        for d in divisors(2 * V):
            F = Fraction(d**3, 1) - (S_frac * Fraction(1, 2)) * d + 2 * V
            if F == 0:
                x_exact = Fraction(d, 1)
                break

    # Solve depressed cubic: x^3 + p x + q = 0 with p = -(S/2), q = 2V
    p = - (S / 2.0)
    q = 2.0 * V
    Delta = (q / 2.0) ** 2 + (p / 3.0) ** 3

    def cbrt(x):
        return math.copysign(abs(x) ** (1.0 / 3.0), x)

    xs = []
    if x_exact is not None:
        xs.append(float(x_exact))

    if Delta >= -1e-15:
        A = -q / 2.0 + math.sqrt(max(0.0, Delta))
        B = -q / 2.0 - math.sqrt(max(0.0, Delta))
        t = cbrt(A) + cbrt(B)
        if t > 0:
            xs.append(t)
    else:
        r = math.sqrt(-p / 3.0)
        theta = math.acos((-q / 2.0) / (r ** 3))
        for k in range(3):
            t = 2 * r * math.cos((theta + 2 * math.pi * k) / 3.0)
            if t > 1e-12:
                xs.append(t)

    # Deduplicate roots
    xs_unique = []
    for t in xs:
        if all(abs(t - u) > 1e-9 for u in xs_unique):
            xs_unique.append(t)

    # Evaluate r^2 for each positive root x with a = V / x^2 and r^2 = (a^2 + 2x^2)/4
    best_r2 = -1.0
    best_x = None
    for x in xs_unique:
        a = V / (x * x)
        r2 = 0.25 * (a * a + 2 * x * x)
        if r2 > best_r2:
            best_r2 = r2
            best_x = x

    # If we have an exact rational root that achieves the max, compute exact p+q
    if x_exact is not None and abs(best_x - float(x_exact)) < 1e-8:
        a_exact = Fraction(V, 1) / (x_exact * x_exact)
        r2_frac = Fraction(1, 4) * (a_exact * a_exact + 2 * (x_exact * x_exact))
        r2_frac = r2_frac.limit_denominator()
        return r2_frac.numerator + r2_frac.denominator
    else:
        # Try to rationalize best_r2; else return the numeric r^2 sum representation p+q not defined
        r2_frac = Fraction(best_r2).limit_denominator(10**12)
        if abs(float(r2_frac) - best_r2) < 1e-10:
            return r2_frac.numerator + r2_frac.denominator
        else:
            return best_r2

solve(54)

# 调用 solve
result = solve(inputs['surface_area'])
print(result)