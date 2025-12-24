inputs = {'OC2_denominator': 16}

def solve(OC2_denominator):
    from fractions import Fraction
    import math

    d = Fraction(OC2_denominator, 1)
    n = Fraction(7, 1)  # Numerator from OC^2 = 7 / d

    # Along AB: OC^2 = 4x^2 - 3x + 3/4. Set equal to 7/d and solve.
    # 4x^2 - 3x + (3/4 - 7/d) = 0
    # Discriminant for ax^2 + bx + c with a=4, b=-3, c=3/4 - 7/d:
    # Δ = b^2 - 4ac = 9 - 16*(3/4 - 7/d) = -3 + 16*(7/d)
    delta = Fraction(16, 1) * n / d - 3

    # Try exact sqrt of delta as Fraction if possible
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
        x_small = (Fraction(3, 1) - s) / 8
        x_large = (Fraction(3, 1) + s) / 8
        # Choose the root inside (0, 1/2) if available, otherwise the one closer to 1/4
        candidates = [x for x in (x_small, x_large) if x > 0 and x < Fraction(1, 2)]
        x = candidates[0] if candidates else min((x_small, x_large), key=lambda t: abs(float(t - Fraction(1, 4))))
        if x.numerator == 1:
            return x.denominator
        # If not a unit fraction, return the nearest integer to its reciprocal
        M = Fraction(x.denominator, x.numerator)
        return M.numerator if M.denominator == 1 else round(float(M))
    else:
        # Fallback to floating arithmetic
        delta_float = float(delta)
        if delta_float < 0:
            # No real solution; fallback: return None-like integer
            return 0
        s = math.sqrt(delta_float)
        x_small = (3 - s) / 8
        x_large = (3 + s) / 8
        x = x_small if 0 < x_small < 0.5 else x_large
        if not (0 < x < 0.5):
            # pick the one closer to 0.25
            x = min([x_small, x_large], key=lambda t: abs(t - 0.25))
        M = 1 / x
        return int(round(M))

solve(OC2_denominator)

# 调用 solve
result = solve(inputs['OC2_denominator'])
print(result)