inputs = {'surface_area': 54}

from fractions import Fraction
import math

def solve(surface_area):
    V = Fraction(23, 1)  # fixed volume
    s2 = Fraction(surface_area, 2)  # ab + bc + ca

    # In the extremal case, two sides are equal: let b=c=x, a=V/x^2.
    # Constraints give cubic: x^3 - s2*x + 2V = 0
    def r2_from_x(xF):
        yF = V / (xF * xF)
        return (yF * yF + 2 * xF * xF) / 4

    # Try Rational Root Theorem on d*x^3 - n*x + 2V*d = 0
    d = s2.denominator
    n = s2.numerator
    const_int = (2 * V * d).numerator
    lead_int = d

    def divisors(n_):
        n_ = abs(int(n_))
        if n_ == 0:
            return {1}
        ds = set()
        r = int(math.isqrt(n_))
        for i in range(1, r + 1):
            if n_ % i == 0:
                ds.add(i)
                ds.add(n_ // i)
        return ds

    rational_roots = []
    for pnum in divisors(const_int):
        for qden in divisors(lead_int):
            for sign in (1, -1):
                xF = Fraction(sign * pnum, qden)
                if xF > 0 and xF**3 - s2 * xF + 2 * V == 0:
                    rational_roots.append(xF)

    if rational_roots:
        best = None
        for xF in rational_roots:
            r2 = r2_from_x(xF)
            if best is None or r2 > best:
                best = r2
        return best.numerator + best.denominator

    # Numeric fallback: solve depressed cubic x^3 + p x + q = 0 with p=-s2, q=2V
    pcoef = -float(s2)
    qcoef = float(2 * V)
    D = (qcoef / 2) ** 2 + (pcoef / 3) ** 3

    def cbrt(z):
        return math.copysign(abs(z) ** (1 / 3), z)

    roots = []
    eps = 1e-15
    if D > eps:
        s = math.sqrt(D)
        u = cbrt(-qcoef / 2 + s)
        v = cbrt(-qcoef / 2 - s)
        roots = [u + v]
    elif D < -eps:
        base = -pcoef / 3
        if base > 0:
            rmag = 2 * math.sqrt(base)
            denom = math.sqrt(base ** 3)
            arg = (-qcoef / 2) / denom if denom != 0 else 1.0
            arg = max(-1.0, min(1.0, arg))
            theta = math.acos(arg)
            roots = [rmag * math.cos((theta + 2 * math.pi * k) / 3) for k in range(3)]
        else:
            roots = [0.0]
    else:
        u = cbrt(-qcoef / 2)
        roots = [2 * u, -u]

    best_r2_val = None
    for x in roots:
        if x > 1e-14:
            xF = Fraction.from_float(x).limit_denominator(10**12)
            r2v = float(r2_from_x(xF))
            if best_r2_val is None or r2v > best_r2_val:
                best_r2_val = r2v

    r2_frac = Fraction(best_r2_val).limit_denominator(10**12)
    return r2_frac.numerator + r2_frac.denominator

solve(54)

# 调用 solve
result = solve(inputs['surface_area'])
print(result)