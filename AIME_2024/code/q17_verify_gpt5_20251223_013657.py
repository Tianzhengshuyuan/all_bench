inputs = {'surface_area': 54}

from fractions import Fraction
import math

def solve(surface_area):
    V = Fraction(23, 1)
    S = Fraction(surface_area).limit_denominator()
    s2 = S / 2  # ab + bc + ca

    def r2_from_x_fraction(xF):
        yF = V / (xF * xF)
        d2 = yF * yF + 2 * xF * xF
        return d2 / 4  # r^2

    def r2_from_x_float(xv):
        yv = float(V) / (xv * xv)
        d2v = yv * yv + 2 * xv * xv
        return d2v / 4

    best_r2 = None

    # Try rational roots first (by RRT): candidates divide 2V
    for r in [1, 2, 23, 46]:
        val = Fraction(r, 1)**3 - s2 * Fraction(r, 1) + 2 * V
        if val == 0 and r > 0:
            r2 = r2_from_x_fraction(Fraction(r, 1))
            r2f = float(r2)
            if best_r2 is None or r2f > best_r2:
                best_r2 = r2f

    # Solve cubic numerically as well to ensure maximal r^2 is found
    # Equation: x^3 - s2*x + 2V = 0  -> depressed cubic: x^3 + p x + q = 0 with p=-s2, q=2V
    p = -float(s2)
    q = float(2 * V)
    disc = (q / 2) ** 2 + (p / 3) ** 3

    roots = []
    if disc >= -1e-15:
        def cbrt(z):
            return math.copysign(abs(z) ** (1 / 3), z)
        A = -q / 2 + math.sqrt(max(disc, 0.0))
        B = -q / 2 - math.sqrt(max(disc, 0.0))
        roots = [cbrt(A) + cbrt(B)]
    else:
        phi = math.acos(-(q / 2) / math.sqrt(- (p / 3) ** 3))
        r_ = 2 * math.sqrt(-p / 3)
        roots = [r_ * math.cos((phi + 2 * math.pi * k) / 3) for k in range(3)]

    for xv in roots:
        if xv > 0:
            r2v = r2_from_x_float(xv)
            if best_r2 is None or r2v > best_r2:
                best_r2 = r2v

    r2_frac = Fraction(best_r2).limit_denominator(10**9)
    return r2_frac.numerator + r2_frac.denominator

solve(54)

# 调用 solve
result = solve(inputs['surface_area'])
print(result)