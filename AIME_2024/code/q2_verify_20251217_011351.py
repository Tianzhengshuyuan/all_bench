inputs = {'x_coord_O': 0}

from fractions import Fraction
import math

def solve(x_coord_O):
    # Points
    xA = Fraction(1, 2)
    yA = Fraction(0, 1)
    xB = Fraction(0, 1)
    # We only need (yB)^2, since yB = sqrt(3)/2 => (yB)^2 = 3/4
    yB_sq = Fraction(3, 4)

    # tan^2(theta0) for line AB (since slope = -tan theta0)
    t2 = yB_sq / (xA - xB) ** 2  # = (3/4) / (1/4) = 3

    # cos(theta0) = 1 / sqrt(1 + tan^2(theta0))
    denom = Fraction(1, 1) + t2  # = 4

    def sqrt_fraction(fr):
        fr = Fraction(fr.numerator, fr.denominator)  # ensure reduced
        n = fr.numerator
        d = fr.denominator
        rn = math.isqrt(n)
        rd = math.isqrt(d)
        if rn * rn == n and rd * rd == d:
            return Fraction(rn, rd)
        # Fallback (shouldn't be needed here)
        return Fraction(math.sqrt(n / d)).limit_denominator(10**12)

    cos_theta0 = Fraction(1, 1) / sqrt_fraction(denom)

    # x-coordinate of the unique point C on AB not covered by other segments
    xC = cos_theta0 ** 3

    # yC^2 = 3 * (1/2 - xC)^2 because yC = sqrt(3) * (1/2 - xC)
    yC_sq = Fraction(3, 1) * (Fraction(1, 2) - xC) ** 2

    # O is at (x_coord_O, 0), so OC^2 = (xC - x_O)^2 + yC^2
    x_O = Fraction(x_coord_O, 1)
    OC_sq = (xC - x_O) ** 2 + yC_sq

    # OC_sq = p/q in lowest terms; return p + q
    p = OC_sq.numerator
    q = OC_sq.denominator
    return p + q

# 调用 solve
result = solve(inputs['x_coord_O'])
print(result)