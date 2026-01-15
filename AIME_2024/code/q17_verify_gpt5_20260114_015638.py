inputs = {'volume': 23}

def solve(volume):
    import math
    from fractions import Fraction

    S2 = 27  # ab + bc + ca fixed by surface area 54
    # Convert volume to Fraction if possible
    V = volume
    if isinstance(V, Fraction):
        Vf = V
    elif isinstance(V, int):
        Vf = Fraction(V, 1)
    elif isinstance(V, float):
        Vf = Fraction.from_float(V).limit_denominator(10**9)
    else:
        try:
            Vf = Fraction(V)
        except:
            Vf = Fraction.from_float(float(V)).limit_denominator(10**9)

    # Feasibility: for ab+bc+ca=27 and a,b,c>0, volume in (0,27]
    Vfloat = float(Vf)
    if Vf <= 0 or Vfloat > 27 + 1e-12:
        return None

    # Try to find an integer root of x^3 - 27x + 2V = 0 when V is integer
    if Vf.denominator == 1:
        Vint = Vf.numerator
        n = abs(2 * Vint)
        # collect divisors of n
        divisors = []
        i = 1
        while i * i <= n:
            if n % i == 0:
                divisors.append(i)
                if i != n // i:
                    divisors.append(n // i)
            i += 1
        roots = []
        for r in divisors:
            if r > 0 and (r * r * r - 27 * r + 2 * Vint == 0):
                roots.append(Fraction(r, 1))
        if roots:
            r = roots[0]
            # Other roots from quadratic factor x^2 + r x + (r^2 - 27) = 0
            disc = Fraction(108, 1) - 3 * r * r
            x_candidates = [r]
            if disc > 0:
                sqrt_disc = math.sqrt(float(disc))
                x2 = (-float(r) + sqrt_disc) / 2.0
                x3 = (-float(r) - sqrt_disc) / 2.0
                if x2 > 1e-12:
                    x_candidates.append(x2)
                if x3 > 1e-12:
                    x_candidates.append(x3)
            r2_best_val = None
            r2_best_frac = None
            for x in x_candidates:
                if isinstance(x, Fraction):
                    y = Vf / (x * x)
                    r2 = (Fraction(2, 1) * x * x + y * y) / 4
                    val = float(r2)
                    if r2_best_val is None or val > r2_best_val:
                        r2_best_val = val
                        r2_best_frac = r2
                else:
                    y = Vfloat / (x * x)
                    r2 = (2 * x * x + y * y) / 4.0
                    if r2_best_val is None or r2 > r2_best_val:
                        r2_best_val = r2
                        r2_best_frac = None
            if r2_best_frac is not None:
                fr = r2_best_frac.limit_denominator()
                return fr.numerator + fr.denominator
            else:
                fr = Fraction.from_float(r2_best_val).limit_denominator(10**12)
                if abs(float(fr) - r2_best_val) <= 1e-10 * max(1.0, r2_best_val):
                    return fr.numerator + fr.denominator
                else:
                    return r2_best_val

    # General case via trigonometric solution (0 < V <= 27)
    t = -Vfloat / 27.0
    t = max(-1.0, min(1.0, t))
    theta = math.acos(t)
    xs = []
    for k in range(3):
        angle = (theta + 2 * math.pi * k) / 3.0
        x = 6.0 * math.cos(angle)
        if x > 1e-12:
            xs.append(x)
    r2_best = -1.0
    for x in xs:
        y = Vfloat / (x * x)
        r2 = (2 * x * x + y * y) / 4.0
        if r2 > r2_best:
            r2_best = r2
    fr = Fraction.from_float(r2_best).limit_denominator(10**12)
    if abs(float(fr) - r2_best) <= 1e-10 * max(1.0, r2_best):
        return fr.numerator + fr.denominator
    else:
        return r2_best

solve(23)

# 调用 solve
result = solve(inputs['volume'])
print(result)