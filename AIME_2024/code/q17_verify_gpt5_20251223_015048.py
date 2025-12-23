inputs = {'surface_area': 54}

def solve(surface_area):
    import math
    from fractions import Fraction

    V = 23  # fixed volume from the problem

    def cbrt(x):
        return math.copysign(abs(x) ** (1.0 / 3.0), x)

    def cubic_real_roots(p, q):
        # Solve x^3 + p x + q = 0
        roots = []
        delta = (q / 2.0) ** 2 + (p / 3.0) ** 3
        if delta >= 0:
            sqrt_delta = math.sqrt(delta)
            u = cbrt(-q / 2.0 + sqrt_delta)
            v = cbrt(-q / 2.0 - sqrt_delta)
            roots.append(u + v)
        else:
            r = math.sqrt(-p / 3.0)
            cos_arg = (-q / 2.0) / (r ** 3)
            # clamp to [-1, 1] to avoid numerical issues
            cos_arg = max(-1.0, min(1.0, cos_arg))
            theta = math.acos(cos_arg)
            for k in range(3):
                roots.append(2 * r * math.cos((theta + 2 * math.pi * k) / 3.0))
        return roots

    # We assume by symmetry that the extremal box has two equal sides: b = c = x, a = V / x^2
    # Constraints reduce to: x^3 - (S/2) x + 2V = 0
    S = surface_area
    p = -S / 2.0
    q = 2.0 * V
    roots = cubic_real_roots(p, q)

    # Keep only positive roots (physical dimensions)
    pos_roots = [r for r in roots if r > 1e-12]

    # Snap to exact integer roots if very close (by Rational Root Theorem, candidates divide 2V)
    def divisors(n):
        n = abs(int(n))
        ds = set()
        i = 1
        while i * i <= n:
            if n % i == 0:
                ds.add(i)
                ds.add(n // i)
            i += 1
        return sorted(ds)

    candidate_ints = divisors(2 * V)
    snapped_roots = []
    for r in pos_roots:
        snapped = r
        for c in candidate_ints:
            if abs(r - c) < 1e-12:
                snapped = float(c)
                break
        snapped_roots.append(snapped)

    # Evaluate objective F = a^2 + b^2 + c^2 = (V/x^2)^2 + 2 x^2 for each root, take max
    best_F = -1.0
    for x in snapped_roots:
        a = V / (x * x)
        F = a * a + 2.0 * x * x
        if F > best_F:
            best_F = F

    r2 = best_F / 4.0
    frac = Fraction(r2).limit_denominator(10**12)
    return frac.numerator + frac.denominator

solve(54)

# 调用 solve
result = solve(inputs['surface_area'])
print(result)