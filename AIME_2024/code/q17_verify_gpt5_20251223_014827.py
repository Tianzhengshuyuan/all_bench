inputs = {'surface_area': 54}

from fractions import Fraction
import math

def solve(surface_area):
    V = Fraction(23, 1)  # fixed volume
    S = Fraction(surface_area).limit_denominator()
    s2 = S / 2  # ab + bc + ca

    # r^2 for the two-equal-edges case (b=c=x, a=y=V/x^2): r^2 = (y^2 + 2x^2)/4
    def r2_from_x_fraction(xF):
        yF = V / (xF * xF)
        d2 = yF * yF + 2 * xF * xF
        return d2 / 4  # r^2

    # Try to find rational roots of x^3 - s2*x + 2V = 0 using integer-coefficient scaling
    # Multiply by den = denom(s2) to get: den*x^3 - num(s2)*x + 2V*den = 0
    den = s2.denominator
    lead_int = den  # integer
    const_int = (2 * V * den).numerator  # integer since V is integer

    def divisors(n):
        n = abs(n)
        if n == 0:
            return {1}
        divs = set()
        r = int(math.isqrt(n))
        for d in range(1, r + 1):
            if n % d == 0:
                divs.add(d)
                divs.add(n // d)
        return divs

    candidates = set()
    for pnum in divisors(const_int):
        for qden in divisors(lead_int):
            candidates.add(Fraction(pnum, qden))
            candidates.add(Fraction(-pnum, qden))

    best_r2_frac = None

    # Test rational candidates exactly
    for xF in candidates:
        if xF <= 0:
            continue
        # Check root for original polynomial x^3 - s2*x + 2V
        if xF**3 - s2 * xF + 2 * V == 0:
            r2 = r2_from_x_fraction(xF)
            if best_r2_frac is None or r2 > best_r2_frac:
                best_r2_frac = r2

    if best_r2_frac is not None:
        return best_r2_frac.numerator + best_r2_frac.denominator

    # If no rational root found, solve cubic numerically (depressed cubic: x^3 + p x + q = 0)
    pcoef = -float(s2)
    qcoef = float(2 * V)
    disc = (qcoef / 2) ** 2 + (pcoef / 3) ** 3

    def cbrt(z):
        return math.copysign(abs(z) ** (1 / 3), z)

    roots = []
    eps = 1e-15
    if disc > eps:
        A = -qcoef / 2 + math.sqrt(disc)
        B = -qcoef / 2 - math.sqrt(disc)
        roots = [cbrt(A) + cbrt(B)]
    else:
        # Three real roots (disc <= 0)
        if -pcoef / 3 <= 0:
            roots = [0.0]
        else:
            rmag = 2 * math.sqrt(-pcoef / 3)
            denom = 2 * math.sqrt((-pcoef / 3) ** 3)
            arg = -qcoef / denom if denom != 0 else 1.0
            arg = max(-1.0, min(1.0, arg))
            phi = math.acos(arg)
            roots = [rmag * math.cos((phi + 2 * math.pi * k) / 3) for k in range(3)]

    best_r2 = None
    for xv in roots:
        if xv > 0:
            # Compute r^2 from float x
            yv = float(V) / (xv * xv)
            d2v = yv * yv + 2 * xv * xv
            r2v = d2v / 4
            if best_r2 is None or r2v > best_r2:
                best_r2 = r2v

    r2_frac = Fraction(best_r2).limit_denominator(10**9)
    return r2_frac.numerator + r2_frac.denominator

solve(surface_area)

# 调用 solve
result = solve(inputs['surface_area'])
print(result)