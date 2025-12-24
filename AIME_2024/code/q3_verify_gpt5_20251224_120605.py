inputs = {'p': '1/115'}

def solve(p):
    from fractions import Fraction
    from math import isqrt

    # Convert input to a Fraction (robust for float/string)
    try:
        f = Fraction(p).limit_denominator(10**9)
    except Exception:
        f = Fraction(str(p)).limit_denominator(10**9)

    if f <= 0 or f > 1:
        return None

    def S_of_N(N):
        return 3 * N * N - 23 * N + 45

    # Build candidate S values near 1/p
    inv = Fraction(1, 1) / f
    candidates_S = set()
    if inv.denominator == 1 and inv.numerator > 0:
        candidates_S.add(inv.numerator)

    # Include approximations for float-like inputs
    try:
        pf = float(p)
        if pf > 0:
            x = 1.0 / pf
            for s in {int(x), int(x) + 1, int(x) - 1, int(round(x))}:
                if s > 0:
                    candidates_S.add(s)
    except Exception:
        pf = None

    # Solve 3N^2 - 23N + 45 = S via discriminant check: D = 12S - 11 must be a perfect square
    for S in sorted(candidates_S):
        D = 12 * S - 11
        if D >= 0:
            r = isqrt(D)
            if r * r == D:
                for num in (23 + r, 23 - r):
                    if num % 6 == 0:
                        N = num // 6
                        if N >= 4 and Fraction(1, S_of_N(N)) == f:
                            return N

    # Fallback: monotone search; p(N) = 1 / S_of_N(N) decreases for N >= 4
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
            if (pf is not None and float(g) < pf) or (pf is None and inv.denominator == 1 and S > inv.numerator):
                break
        N += 1

    return None

solve(1/115)

# 调用 solve
result = solve(inputs['p'])
print(result)