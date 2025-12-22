inputs = {'volume': 23}

def solve(volume):
    from math import acos, cos, pi, isfinite, sqrt, isclose, isqrt
    from fractions import Fraction

    v = volume

    # Surface area constraint: ab + bc + ca = 27
    # Under Lagrange multipliers, the extremum occurs when two sides are equal: let b=c=x, a=y.
    # Then: x^2 + 2xy = 27 and x^2*y = v => cubic for x: x^3 - 27x + 2v = 0

    def best_r2_from_roots(roots, vfloat):
        best = None
        for x in roots:
            if x > 1e-12 and isfinite(x):
                y = vfloat / (x * x)
                S = y * y + 2.0 * x * x
                r2 = S / 4.0
                if best is None or r2 > best:
                    best = r2
        return best

    # Try to find an integer root first (when volume is integer), to allow exact fraction computation
    best_frac = None
    if isinstance(v, int) or (isinstance(v, Fraction) and v.denominator == 1):
        vint = int(v)
        # Rational root theorem: integer roots divide 2*v
        N = abs(2 * vint)
        if N != 0:
            int_roots = set()
            for d in range(1, isqrt(N) + 1):
                if N % d == 0:
                    for cand in (d, N // d):
                        for sign in (1, -1):
                            x = sign * cand
                            if x * x * x - 27 * x + 2 * vint == 0:
                                int_roots.add(x)
            # If we found any integer roots, analyze them and their companion quadratic roots
            if int_roots:
                # Collect positive roots (integer and companion) and compute r^2 values
                roots = []
                exact_candidates = []  # (r2_fraction, r2_float) for integer-root cases
                for r in int_roots:
                    # Companion quadratic: x^2 + r x + (r^2 - 27) = 0
                    # Discriminant:
                    D = 108 - 3 * (r * r)
                    if D >= 0:
                        sqrtD = sqrt(D)
                        x1 = (-r + sqrtD) / 2.0
                        x2 = (-r - sqrtD) / 2.0
                        roots.extend([x1, x2])
                    # Include the integer root itself
                    roots.append(float(r))
                    # For the integer root r, compute exact r^2 as Fraction
                    if r > 0:
                        y = Fraction(vint, r * r)
                        S = y * y + Fraction(2 * r * r, 1)
                        r2_frac = S / 4
                        exact_candidates.append((r2_frac, float(r2_frac)))
                # Among all positive roots, pick the maximum r^2
                # First compute numeric maxima
                vfloat = float(vint)
                r2_numeric = best_r2_from_roots(roots, vfloat)
                # If any exact candidates exist, see if one matches the numeric maximum (within tolerance)
                if exact_candidates:
                    # Pick the exact candidate with largest float value
                    r2_exact_best = max(exact_candidates, key=lambda t: t[1])
                    # Compare which is larger: numeric from all roots vs this exact integer-root candidate
                    if r2_numeric is None or r2_exact_best[1] >= r2_numeric - 1e-12:
                        best_frac = r2_exact_best[0]
                    else:
                        # No exact candidate is maximum; proceed with numeric best
                        pass

                if best_frac is not None:
                    # We have exact fraction for the maximum r^2; return p+q
                    return best_frac.numerator + best_frac.denominator

    # Fallback: use trigonometric solution for cubic (valid since v <= 27 due to SA fixed)
    vfloat = float(v)
    # Clamp acos argument
    t = -vfloat / 27.0
    if t < -1.0:
        t = -1.0
    if t > 1.0:
        t = 1.0
    theta = acos(t)
    roots = []
    for k in range(3):
        xk = 6.0 * cos((theta - 2.0 * pi * k) / 3.0)
        if xk > 1e-12:
            roots.append(xk)

    r2_best = best_r2_from_roots(roots, vfloat)

    # Convert to a simple fraction; for the given problem (v=23) this will be 657/64 exactly
    frac = Fraction(r2_best).limit_denominator(10**9)
    return frac.numerator + frac.denominator

# 调用 solve
result = solve(inputs['volume'])
print(result)