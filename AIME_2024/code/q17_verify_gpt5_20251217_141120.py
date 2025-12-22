inputs = {'volume': 23}

from fractions import Fraction
import math

def solve(volume):
    P = Fraction(27, 1)  # ab + bc + ca = 27 from surface area 54
    V = Fraction(volume, 1)

    # Cubic: x^3 - P x + 2V = 0
    def f_val(x_float):
        return x_float**3 - float(P) * x_float + 2.0 * float(V)

    # Try to find an integer root (by Rational Root Theorem, any rational root is integer)
    x_candidates = []
    if V.denominator == 1:
        M = abs(2 * V.numerator)
        # enumerate positive divisors
        for d in range(1, int(math.isqrt(M)) + 1):
            if M % d == 0:
                for cand in (d, M // d):
                    for sign in (1, -1):
                        x = sign * cand
                        # exact check using Fractions
                        if Fraction(x, 1)**3 - P * Fraction(x, 1) + 2 * V == 0:
                            if x > 0:
                                x_candidates.append(Fraction(x, 1))
        x_candidates = sorted(set(x_candidates))

    x_small = None

    # Prefer the smaller positive root in (0, 3], which yields the maximal diagonal
    if x_candidates:
        pos = [x for x in x_candidates if x > 0]
        if pos:
            # If there are multiple, the smallest positive one is the one in (0,3]
            x_small = min(pos)

    if x_small is None:
        # Use bisection to find the root in (0, 3] (exists for 0 < V <= 27)
        # Handle special case: V=27 gives root exactly at 3
        if V == 27:
            x_small = Fraction(3, 1)
        else:
            a, b = 0.0, 3.0
            fa, fb = f_val(a), f_val(b)
            # ensure sign change
            if fa * fb > 0:
                # fallback widen interval if needed
                b = 5.0
                fb = f_val(b)
            # bisection
            for _ in range(200):
                m = (a + b) / 2.0
                fm = f_val(m)
                if fa * fm <= 0:
                    b, fb = m, fm
                else:
                    a, fa = m, fm
            x_small = Fraction.from_float((a + b) / 2.0).limit_denominator(10**12)

    # With b=c=x_small and a=V/x^2, compute r^2 = (a^2 + b^2 + c^2)/4
    x = x_small
    a = V / (x * x)
    b = x
    c = x
    d2 = a * a + b * b + c * c
    r2 = d2 / 4

    r2 = Fraction(r2.numerator, r2.denominator)  # reduce
    return r2.numerator + r2.denominator

# 调用 solve
result = solve(inputs['volume'])
print(result)