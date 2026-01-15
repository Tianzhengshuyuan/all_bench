inputs = {'volume': 23}

from fractions import Fraction
from math import acos, cos, pi

def solve(volume):
    # Maximize a^2+b^2+c^2 subject to ab+bc+ca=27 and abc=volume.
    # By symmetry, at optimum two edges are equal: a=b=x, c=y.
    # Then: x^2 + 2xy = 27 and x^2*y = V.
    # Eliminating y gives cubic in x: x^3 - 27x + 2V = 0.
    # For each positive real root x, y = V/x^2, and the squared diagonal is S = 2x^2 + y^2.
    # The required r^2 is max(S)/4 over the positive roots.
    V = Fraction(volume)

    def F(x):
        return x**3 - 27*x + 2*V

    # Try exact rational roots first (Rational Root Theorem)
    def divisors(n):
        n = abs(n)
        ds = set()
        i = 1
        while i * i <= n:
            if n % i == 0:
                ds.add(i)
                ds.add(n // i)
            i += 1
        return ds

    roots_exact = []
    twoV = 2 * V
    num, den = twoV.numerator, twoV.denominator
    if num != 0:
        Ps = divisors(abs(num))
        Qs = divisors(den)
        for p in Ps:
            for q in Qs:
                for s in (1, -1):
                    x = Fraction(s * p, q)
                    if x <= 0:
                        continue
                    if F(x) == 0 and x not in roots_exact:
                        roots_exact.append(x)

    candidates = []

    # From exact roots, compute r^2 exactly
    for x in roots_exact:
        y = V / (x * x)
        if y <= 0:
            continue
        S = 2 * x * x + y * y
        r2 = S / 4
        candidates.append(('exact', r2))

    # Numeric roots via trigonometric formula when 0 < V <= 27 (feasible region)
    V_float = float(V)
    if V_float > 0:
        if V_float <= 27 + 1e-12:
            # For cubic x^3 + px + q with p=-27, q=2V:
            # Roots: 2*sqrt(-p/3)*cos((arccos((3q/2p)*sqrt(-3/p)) + 2kπ)/3), k=0,1,2
            arg = -V_float / 27.0
            if arg < -1.0:
                arg = -1.0
            if arg > 1.0:
                arg = 1.0
            phi = acos(arg)
            for k in (0, 1, 2):
                x = 6.0 * cos((phi + 2 * pi * k) / 3.0)
                if x > 1e-12:
                    y = V_float / (x * x)
                    if y <= 0:
                        continue
                    S = 2 * x * x + y * y
                    r2 = S / 4.0
                    candidates.append(('float', r2))

    if not candidates:
        return None

    # Choose maximal r^2, preferring exact if tied
    best_exact = None
    best_float = None
    for typ, r2 in candidates:
        if typ == 'exact':
            if best_exact is None or r2 > best_exact:
                best_exact = r2
        else:
            if best_float is None or r2 > best_float:
                best_float = r2

    if best_exact is not None and (best_float is None or float(best_exact) >= best_float - 1e-12):
        r2 = best_exact.limit_denominator()
        return r2.numerator + r2.denominator
    else:
        r2_frac = Fraction(best_float).limit_denominator(10**12)
        return r2_frac.numerator + r2_frac.denominator

volume = 23
solve(volume)

# 调用 solve
result = solve(inputs['volume'])
print(result)