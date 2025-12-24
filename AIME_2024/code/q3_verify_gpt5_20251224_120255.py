inputs = {'p': '1/115'}

def solve(p):
    from fractions import Fraction
    from math import isqrt

    # Convert p to a rational fraction
    try:
        f = Fraction(p).limit_denominator(10**9)
    except Exception:
        f = Fraction(str(p)).limit_denominator(10**9)

    if f <= 0 or f > 1:
        return None

    def S_of_N(N):
        return 3 * N * N - 23 * N + 45

    # Try algebraic solution using S = 1/p
    inv = Fraction(1, 1) / f
    if inv.denominator == 1 and inv.numerator > 0:
        S = inv.numerator
        D = 12 * S - 11
        if D >= 0:
            r = isqrt(D)
            if r * r == D:
                for num in (23 + r, 23 - r):
                    if num % 6 == 0:
                        N = num // 6
                        if N >= 4 and Fraction(1, S_of_N(N)) == f:
                            return N

    # Fallback: monotone search since p(N) = 1 / (3N^2 - 23N + 45) decreases for N >= 4
    try:
        pf = float(p)
    except Exception:
        pf = None

    N = 4
    maxN = 10**6
    while N <= maxN:
        S = S_of_N(N)
        if S > 0:
            g = Fraction(1, S)
            if g == f:
                return N
            if pf is not None and abs(float(g) - pf) <= 1e-12 * max(1.0, abs(pf)):
                return N
            if (pf is not None and float(g) < pf) or (pf is None and g < f):
                break
        N += 1

    return None

solve(1/115)

# 调用 solve
result = solve(inputs['p'])
print(result)