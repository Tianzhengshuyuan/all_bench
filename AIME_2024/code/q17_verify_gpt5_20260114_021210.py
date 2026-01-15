inputs = {'volume': 23}

from fractions import Fraction
from math import acos, cos, pi

def solve(volume):
    V = Fraction(volume)

    # Feasible range for positive edges with ab+bc+ca=27 is 0 < V <= 27
    if V <= 0 or V > 27:
        return None

    V_float = float(V)
    # Trigonometric solution for depressed cubic x^3 - 27x + 2V = 0
    arg = -V_float / 27.0
    if arg < -1.0:
        arg = -1.0
    if arg > 1.0:
        arg = 1.0
    theta = acos(arg)

    best = None
    for k in (0, 1, 2):
        x = 6.0 * cos((theta + 2 * pi * k) / 3.0)
        if x > 1e-15:
            y = V_float / (x * x)
            if y > 0:
                r2 = (2.0 * x * x + y * y) / 4.0
                if best is None or r2 > best:
                    best = r2

    if best is None:
        return None

    r2_frac = Fraction(best).limit_denominator(10**12)
    return r2_frac.numerator + r2_frac.denominator

volume = 23
solve(volume)

# 调用 solve
result = solve(inputs['volume'])
print(result)