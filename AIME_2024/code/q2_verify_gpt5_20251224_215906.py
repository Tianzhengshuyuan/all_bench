inputs = {'OC2_denominator': 16}

def solve(OC2_denominator):
    from fractions import Fraction
    import math

    d = Fraction(OC2_denominator, 1)

    # On AB: y = -sqrt(3)x + sqrt(3)/2, so OC^2 = x^2 + y^2 = 4x^2 - 3x + 3/4
    # Set 4x^2 - 3x + 3/4 = 7/d and solve for x.
    a = Fraction(4, 1)
    b = Fraction(-3, 1)
    c = Fraction(3, 4) - Fraction(7, 1) / d
    delta = b * b - 4 * a * c  # Discriminant

    def sqrt_fraction(fr):
        if fr < 0:
            return None
        num, den = fr.numerator, fr.denominator
        sn, sd = math.isqrt(num), math.isqrt(den)
        if sn * sn == num and sd * sd == den:
            return Fraction(sn, sd)
        return None

    s = sqrt_fraction(delta)
    if s is not None:
        # x = (-b ± sqrt(delta)) / (2a); here -b = 3, 2a = 8
        x1 = (Fraction(3, 1) - s) / 8
        x2 = (Fraction(3, 1) + s) / 8
        # Choose the root strictly between 0 and 1/2 (point on AB, not endpoints)
        candidates = [x for x in (x1, x2) if x > 0 and x < Fraction(1, 2)]
        x = candidates[0] if candidates else min((x1, x2), key=lambda t: abs(float(t - Fraction(1, 4))))
        if x.numerator == 1:
            return x.denominator
        inv = Fraction(x.denominator, x.numerator)
        if inv.denominator == 1:
            return inv.numerator
        return int(round(float(inv)))
    else:
        # Fallback to floating arithmetic if sqrt not rational
        s_float = math.sqrt(float(delta))
        x1 = (3 - s_float) / 8.0
        x2 = (3 + s_float) / 8.0
        candidates = [x for x in (x1, x2) if 0 < x < 0.5]
        x = candidates[0] if candidates else min((x1, x2), key=lambda t: abs(t - 0.25))
        return int(round(1.0 / x))

OC2_denominator = 16
solve(OC2_denominator)

# 调用 solve
result = solve(inputs['OC2_denominator'])
print(result)