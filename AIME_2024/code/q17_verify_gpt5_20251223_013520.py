inputs = {'surface_area': 54}

from fractions import Fraction
import math

def solve(surface_area):
    V = Fraction(23, 1)
    S = Fraction(surface_area).limit_denominator()
    s2 = S / 2  # ab + bc + ca

    # Solve for the "antioptimal" box with two equal edges: let b = c = x, a = y
    # Constraints:
    #   x^2 + 2xy = s2
    #   x^2 y = V  => y = V / x^2
    # Cubic in x: x^3 - s2*x + 2V = 0
    def r2_from_x(x_val):
        xF = Fraction(x_val, 1) if isinstance(x_val, int) else Fraction(x_val).limit_denominator()
        yF = V / (xF * xF)
        d2 = yF * yF + 2 * xF * xF
        return d2 / 4  # r^2

    # Try rational roots first (by RRT): candidates divide 2V
    candidates = [1, 2, 23, 46]
    best_r2_frac = None
    for r in candidates:
        val = Fraction(r, 1)**3 - s2 * Fraction(r, 1) + 2 * V
        if val == 0 and r > 0:
            r2 = r2_from_x(r)
            if best_r2_frac is None or r2 > best_r2_frac:
                best_r2_frac = r2

    if best_r2_frac is not None:
        return best_r2_frac.numerator + best_r2_frac.denominator

    # If no rational root, solve cubic numerically and pick positive root maximizing r^2
    p = -float(s2)
    q = float(2 * V)
    disc = (q / 2) ** 2 + (p / 3) ** 3

    roots = []
    if disc >= 0:
        def cbrt(z):
            return math.copysign(abs(z) ** (1 / 3), z)
        A = -q / 2 + math.sqrt(disc)
        B = -q / 2 - math.sqrt(disc)
        roots = [cbrt(A) + cbrt(B)]
    else:
        phi = math.acos(-(q / 2) / math.sqrt(- (p / 3) ** 3))
        r_ = 2 * math.sqrt(-p / 3)
        roots = [r_ * math.cos((phi + 2 * math.pi * k) / 3) for k in range(3)]

    best_r2 = None
    for xv in roots:
        if xv > 0:
            yv = float(V) / (xv * xv)
            d2v = yv * yv + 2 * xv * xv
            r2v = d2v / 4
            if best_r2 is None or r2v > best_r2:
                best_r2 = r2v

    # Convert to fraction (best effort); return p+q
    r2_frac = Fraction(best_r2).limit_denominator(10**9)
    return r2_frac.numerator + r2_frac.denominator

solve(surface_area)

# 调用 solve
result = solve(inputs['surface_area'])
print(result)