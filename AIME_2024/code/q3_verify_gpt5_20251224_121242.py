inputs = {'p': '1/115'}

def solve(p):
    from fractions import Fraction
    from math import isqrt, sqrt

    # Convert p to a Fraction robustly
    try:
        f = Fraction(p).limit_denominator(10**12)
    except Exception:
        f = Fraction(str(p)).limit_denominator(10**12)

    if f <= 0 or f > 1:
        return None

    def S_of_N(N):
        return 3 * N * N - 23 * N + 45

    def p_of_N(N):
        s = S_of_N(N)
        if s <= 0:
            return None
        return Fraction(1, s)

    # Helper for float-like comparisons
    try:
        pf = float(p)
    except Exception:
        pf = None

    def matches(g):
        if g is None:
            return False
        if pf is None:
            return g == f
        return abs(float(g) - pf) <= 1e-12 * max(1.0, abs(pf))

    # Build candidate S values near 1/p
    inv = Fraction(1, 1) / f
    candidates_S = set()
    if inv.denominator == 1 and inv.numerator > 0:
        candidates_S.add(inv.numerator)
    if pf is not None and pf > 0:
        x = 1.0 / pf
        for s in {int(x), int(round(x)), int(x) + 1, int(x) - 1, int(x) + 2, int(x) - 2}:
            if s > 0:
                candidates_S.add(s)

    # Solve 3N^2 - 23N + 45 = S via discriminant check: D = 12S - 11 must be a perfect square
    for S in sorted(candidates_S):
        D = 12 * S - 11
        if D >= 0:
            r = isqrt(D)
            if r * r == D:
                for num in (23 + r, 23 - r):
                    if num % 6 == 0:
                        N = num // 6
                        if N >= 4 and matches(p_of_N(N)) and S_of_N(N) == S:
                            return N

    # Fallback: local search around approximate N from quadratic formula if pf is available
    if pf is not None and pf > 0:
        try:
            S_est = 1.0 / pf
            D_est = max(0.0, 12.0 * S_est - 11.0)
            N_est = int(round((23.0 + sqrt(D_est)) / 6.0))
        except Exception:
            N_est = 4
        low = max(4, N_est - 10000)
        high = max(low, N_est + 10000)
        for N in range(low, high + 1):
            if matches(p_of_N(N)):
                return N

    # Last resort: monotone search from N=4; p(N) decreases with N for N >= 4
    N = 4
    maxN = 10**6
    while N <= maxN:
        g = p_of_N(N)
        if matches(g):
            return N
        if pf is not None and g is not None and float(g) < pf:
            break
        if pf is None and g is not None and g < f:
            break
        N += 1

    return None

solve(1/115)

# 调用 solve
result = solve(inputs['p'])
print(result)