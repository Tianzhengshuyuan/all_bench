inputs = {'volume': 23}

from fractions import Fraction
import math

def solve(volume):
    V = volume

    if V is None:
        return None
    if isinstance(V, (int,)) and V <= 0:
        return None

    def integer_divisors(n):
        n = abs(n)
        divs = set()
        for d in range(1, int(math.isqrt(n)) + 1):
            if n % d == 0:
                divs.add(d)
                divs.add(n // d)
        return sorted(divs)

    # Try to find positive integer roots of a^3 - 27a + 2V = 0
    pos_roots = []
    if isinstance(V, int):
        for a in integer_divisors(2 * V):
            if a > 0:
                if a * a * a - 27 * a + 2 * V == 0:
                    pos_roots.append(a)

    def r2_from_a_fraction(V, a):
        A = Fraction(a, 1)
        L = Fraction(V, 1) / (A * A)
        D2 = 2 * (A * A) + L * L
        r2 = D2 / 4
        return r2

    if pos_roots:
        # Among valid roots, choose the one that maximizes the space diagonal
        best_r2 = None
        for a in pos_roots:
            r2 = r2_from_a_fraction(V, a)
            if best_r2 is None or r2 > best_r2:
                best_r2 = r2
        return best_r2.numerator + best_r2.denominator

    # Numeric fallback for general V (0 < V <= 27)
    V_float = float(V)
    if not (V_float > 0):
        return None

    def g(a):
        return a ** 3 - 27 * a + 2 * V_float

    # Handle V close to 27 (cube)
    if abs(2 * V_float - 54) <= 1e-12:
        # Cube with side s where SA=54 => s=3
        # D^2 = 3*s^2 = 27, r^2 = 27/4
        r2 = Fraction(27, 4)
        return r2.numerator + r2.denominator

    if V_float > 27 + 1e-12:
        return None  # infeasible with SA fixed at 54

    def bisection(lo, hi, f, tol=1e-14, itmax=200):
        flo, fhi = f(lo), f(hi)
        if abs(flo) <= 1e-18:
            return lo
        if abs(fhi) <= 1e-18:
            return hi
        if flo * fhi > 0:
            return None
        for _ in range(itmax):
            mid = (lo + hi) / 2.0
            fmid = f(mid)
            if abs(fmid) <= tol:
                return mid
            if flo * fmid < 0:
                hi, fhi = mid, fmid
            else:
                lo, flo = mid, fmid
        return (lo + hi) / 2.0

    # First root in (0, 3)
    eps = 1e-12
    a1 = bisection(eps, 3.0, g)
    # Second root in (3, hi)
    hi = 4.0
    while g(hi) <= 0:
        hi *= 2.0
    a2 = bisection(3.0, hi, g)

    def r2_from_a_float(a):
        D2 = 2 * a * a + (V_float / (a * a)) ** 2
        return D2 / 4.0

    candidates = []
    if a1 is not None and a1 > 0:
        candidates.append(r2_from_a_float(a1))
    if a2 is not None and a2 > 0:
        candidates.append(r2_from_a_float(a2))
    if not candidates:
        return None
    r2_best = max(candidates)

    # Try to rationalize if possible
    r2_frac = Fraction(r2_best).limit_denominator(10**9)
    return r2_frac.numerator + r2_frac.denominator

solve(volume)

# 调用 solve
result = solve(inputs['volume'])
print(result)