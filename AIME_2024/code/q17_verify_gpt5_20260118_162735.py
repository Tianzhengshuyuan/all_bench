inputs = {'volume': 23}

def solve(volume):
    from fractions import Fraction
    import math

    P = 27  # ab + bc + ca
    V = volume

    # Try to find integer rational roots of a^3 - P a + 2V = 0 (with leading coeff 1)
    roots_int = []
    V_int = None
    if isinstance(V, int):
        V_int = V
    elif isinstance(V, float) and abs(V - round(V)) < 1e-12:
        V_int = int(round(V))

    if V_int is not None:
        n = abs(2 * V_int)
        if n != 0:
            divs = set()
            i = 1
            while i * i <= n:
                if n % i == 0:
                    divs.add(i)
                    divs.add(n // i)
                i += 1
            for d in divs:
                if d > 0:
                    if d**3 - P * d + 2 * V_int == 0:
                        roots_int.append(d)

    if roots_int:
        best_r2 = None
        for a in roots_int:
            s = Fraction(2 * a, 1) + Fraction(V_int, a * a)  # s = x + y + z with x=y=a, z=V/a^2
            D2 = s * s - 2 * P
            r2 = D2 / 4
            if best_r2 is None or r2 > best_r2:
                best_r2 = r2
        return best_r2.numerator + best_r2.denominator

    # Fallback: numeric solve via Cardano for depressed cubic a^3 + p a + q = 0
    p = -P
    q = 2.0 * float(V)
    Δ = (q / 2.0) ** 2 + (p / 3.0) ** 3

    def cbrt(x):
        return math.copysign(abs(x) ** (1.0 / 3.0), x)

    pos_roots = []
    if Δ >= 0:
        sqrtΔ = math.sqrt(Δ)
        u = cbrt(-q / 2.0 + sqrtΔ)
        v = cbrt(-q / 2.0 - sqrtΔ)
        x = u + v
        if x > 0:
            pos_roots.append(x)
    else:
        r = 2.0 * math.sqrt(-p / 3.0)
        phi = math.acos((-q / 2.0) / math.sqrt((-p / 3.0) ** 3))
        for k in range(3):
            x = r * math.cos((phi + 2.0 * math.pi * k) / 3.0)
            if x > 0:
                pos_roots.append(x)

    if not pos_roots:
        # No feasible positive root; return 0 by convention
        return 0

    best_r2_float = None
    for a in pos_roots:
        s = 2.0 * a + float(V) / (a * a)
        D2 = s * s - 2.0 * P
        r2 = D2 / 4.0
        if best_r2_float is None or r2 > best_r2_float:
            best_r2_float = r2

    r2_frac = Fraction(best_r2_float).limit_denominator(10**9)
    return r2_frac.numerator + r2_frac.denominator

# 调用 solve
result = solve(inputs['volume'])
print(result)