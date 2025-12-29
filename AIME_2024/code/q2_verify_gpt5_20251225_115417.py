from fractions import Fraction
inputs = {'oc2': Fraction(7, 16)}

from fractions import Fraction
from math import isqrt

def solve(oc2):
    oc2 = Fraction(oc2)

    def sqrt_fraction(fr):
        if fr < 0:
            raise ValueError("Negative radicand")
        num = fr.numerator
        den = fr.denominator
        s_num = isqrt(num)
        s_den = isqrt(den)
        if s_num * s_num == num and s_den * s_den == den:
            return Fraction(s_num, s_den)
        else:
            raise ValueError("Non-square radicand for exact Fraction sqrt")
    
    rad = 16 * oc2 - 3
    s = sqrt_fraction(rad)
    x1 = (Fraction(3) + s) / 8
    x2 = (Fraction(3) - s) / 8

    valid = [x for x in (x1, x2) if x > 0 and x < Fraction(1, 2)]
    if not valid:
        # Fall back: if one is in (0,1], pick the one < 1 to stay on/near segment AB
        valid = [x for x in (x1, x2) if x > 0 and x <= Fraction(1, 2)]
    if not valid:
        # As a last resort, pick the one closer to the segment [0,1/2]
        # This ensures a deterministic choice if inputs are atypical
        def dist_to_segment(x):
            if x < 0:
                return -x
            if x > Fraction(1, 2):
                return x - Fraction(1, 2)
            return Fraction(0)
        x = min((x1, x2), key=dist_to_segment)
    else:
        # If two valid, pick the smaller (consistent with the intended unique point for this setup)
        x = min(valid)

    if x == 0 or x == Fraction(1, 2):
        raise ValueError("C coincides with A or B, invalid for this problem")

    num = x.numerator
    den = x.denominator
    if den % num != 0:
        raise ValueError("x is not of the form 1/N with integer N")
    N = den // num
    return N

solve(Fraction(7, 16))

# 调用 solve
result = solve(inputs['oc2'])
print(result)