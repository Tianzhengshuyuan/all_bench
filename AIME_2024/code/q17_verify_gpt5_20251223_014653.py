inputs = {'surface_area': 54}

from fractions import Fraction
import math

def solve(surface_area):
    V = Fraction(23, 1)  # fixed volume
    S = Fraction(surface_area).limit_denominator()
    s2 = S / 2  # ab + bc + ca

    # For the extremal box, two sides are equal: let b = c = x, a = y = V/x^2
    # Constraint: x^2 + 2xy = s2 -> x^2 + 2V/x = s2 -> x^3 - s2*x + 2V = 0
    def r2_from_x_fraction(xF):
        yF = V / (xF * xF)
        d2 = yF * yF + 2 * xF * xF
        return d2 / 4  # r^2

    # Rational Root Theorem on integer-coefficient scaled cubic
    # den*x^3 - num(s2)*x + 2V*den = 0
    den = s2.denominator
    lead_int = den
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

    rational_roots = []
    for pnum in divisors(const_int):
        for qden in divisors(lead_int):
            for sign in (1, -1):
                xF = Fraction(sign * pnum, qden)
                if xF > 0 and xF**3 - s2 * xF + 2 * V == 0:
                    rational_roots.append(xF)

    # Numeric solver for depressed cubic x^3 + p x + q = 0
    def cubic_real_roots(p, q):
        D = (q / 2) ** 2 + (p / 3) ** 3
        eps = 1e-15
        roots = []
        if D > eps:
            s = math.sqrt(D)
            def cbrt(z):
                return math.copysign(abs(z) ** (1 / 3), z)
            u = cbrt(-q / 2 + s)
            v = cbrt(-q / 2 - s)
            roots = [u + v]
        elif D < -eps:
            r = 2 * math.sqrt(-p / 3)
            theta = math.acos(max(-1.0, min(1.0, (-q / 2) / math.sqrt(- (p / 3) ** 3))))
            roots = [r * math.cos((theta + 2 * k * math.pi) / 3) for k in range(3)]
        else:
            # multiple root case
            if q == 0:
                roots = [0.0]
            else:
                u = math.copysign(abs(-q / 2) ** (1 / 3), -q / 2)
                roots = [2 * u, -u]
        return roots

    # Evaluate candidates numerically
    pcoef = -float(s2)
    qcoef = float(2 * V)
    numeric_roots = cubic_real_roots(pcoef, qcoef)
    best_r2_num = None
    for xv in numeric_roots:
        if xv > 0:
            yv = float(V) / (xv * xv)
            d2v = yv * yv + 2 * xv * xv
            r2v = d2v / 4
            if best_r2_num is None or r2v > best_r2_num:
                best_r2_num = r2v

    # Check rational roots for exact r^2 and see if any achieves the numeric maximum
    best_r2_frac = None
    for xF in rational_roots:
        r2F = r2_from_x_fraction(xF)
        if best_r2_frac is None or r2F > best_r2_frac:
            best_r2_frac = r2F

    # Prefer exact fraction if it matches the numeric maximum (within tolerance)
    if best_r2_frac is not None:
        if best_r2_num is None or abs(float(best_r2_frac) - best_r2_num) <= 1e-10 or float(best_r2_frac) > best_r2_num - 1e-12:
            r2_final = best_r2_frac
            return r2_final.numerator + r2_final.denominator

    # Fallback: rationalize the numeric maximum
    from fractions import Fraction as Fr
    r2_frac_approx = Fr(best_r2_num).limit_denominator(10**9)
    return r2_frac_approx.numerator + r2_frac_approx.denominator

solve(54)

# 调用 solve
result = solve(inputs['surface_area'])
print(result)