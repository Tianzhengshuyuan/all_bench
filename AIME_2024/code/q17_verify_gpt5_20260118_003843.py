inputs = {'volume': 23}

from fractions import Fraction

def solve(volume):
    V = volume

    if V is None:
        return None

    # For feasibility with fixed surface area 54, maximum volume is at the cube with side 3 -> V=27
    V_float = float(V)
    if V_float <= 0:
        return None
    if V_float > 27 + 1e-12:
        return None

    # Special cube case: V = 27 -> side = 3 -> diagonal^2 = 27 -> r^2 = 27/4
    if abs(V_float - 27.0) <= 1e-12:
        r2 = Fraction(27, 4)
        return r2.numerator + r2.denominator

    # We consider boxes with two equal sides a, a and the third side L.
    # Constraints: a^2 L = V, and a^2 + 2 a L = 27.
    # Eliminating L gives cubic in a: a^3 - 27 a + 2V = 0.
    def f(a):
        return a**3 - 27.0*a + 2.0*V_float

    def bisection(lo, hi, func, tol=1e-14, itmax=200):
        flo, fhi = func(lo), func(hi)
        if flo == 0:
            return lo
        if fhi == 0:
            return hi
        if flo * fhi > 0:
            return None
        for _ in range(itmax):
            mid = (lo + hi) / 2.0
            fmid = func(mid)
            if abs(fmid) <= tol:
                return mid
            if flo * fmid < 0:
                hi, fhi = mid, fmid
            else:
                lo, flo = mid, fmid
        return (lo + hi) / 2.0

    # Find two positive roots in (0,3) and (3,∞)
    # For 0 < V < 27, we have f(0)>0, f(3)=2V-54<0, so a root in (0,3).
    a1 = bisection(1e-12, 3.0, f)
    # For the second root, start above 3 and expand until sign changes
    hi = 4.0
    while f(hi) <= 0:
        hi *= 2.0
    a2 = bisection(3.0, hi, f)

    def r2_from_a(a):
        # L = V / a^2
        L = V_float / (a*a)
        D2 = 2.0*a*a + L*L
        return D2 / 4.0

    candidates = []
    if a1 is not None and a1 > 0:
        candidates.append(r2_from_a(a1))
    if a2 is not None and a2 > 0:
        candidates.append(r2_from_a(a2))
    if not candidates:
        return None

    r2_best = max(candidates)
    r2_frac = Fraction(r2_best).limit_denominator(10**9)
    return r2_frac.numerator + r2_frac.denominator

volume = 23
solve(volume)

# 调用 solve
result = solve(inputs['volume'])
print(result)