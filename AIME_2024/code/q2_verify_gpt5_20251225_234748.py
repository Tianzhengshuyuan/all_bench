from fractions import Fraction
inputs = {'OC2': Fraction(7, 16)}

from fractions import Fraction
from math import isqrt

def _sqrt_fraction(fr):
    if fr < 0:
        return None
    n = fr.numerator
    d = fr.denominator
    sn = isqrt(n)
    sd = isqrt(d)
    if sn * sn == n and sd * sd == d:
        return Fraction(sn, sd)
    return None

def solve(OC2):
    # Try to infer L from the relation OC2 = (L^4 - 6 L^2 + 12)/16
    # Let t = L^2. Then 16*OC2 = t^2 - 6t + 12 -> t^2 - 6t + (12 - 16*OC2) = 0
    S = OC2
    disc = Fraction(64, 1) * S - Fraction(12, 1)  # discriminant Δ = 64*S - 12
    sd = _sqrt_fraction(disc)
    if sd is not None:
        t1 = (Fraction(6, 1) + sd) / 2
        t2 = (Fraction(6, 1) - sd) / 2
        candidates = [t for t in (t1, t2) if t >= 0]
        # Prefer the case where AB is in the family: L^2 = |AB|^2 = 1
        for t in candidates:
            if t == Fraction(1, 1):
                return Fraction(1, 1)
        # Otherwise, choose the smaller positive t and return its sqrt if rational
        if candidates:
            t = min(candidates)
            st = _sqrt_fraction(t)
            if st is not None:
                return st
    # Fallback: AB must be in the family, hence L = |AB| = sqrt((1/2)^2 + (√3/2)^2) = 1
    return Fraction(1, 1)

solve(Fraction(7, 16))

# 调用 solve
result = solve(inputs['OC2'])
print(result)