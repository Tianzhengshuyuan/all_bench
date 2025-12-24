inputs = {'p': '1/115'}

def solve(p):
    from fractions import Fraction
    from math import isqrt, sqrt

    # Convert p to a Fraction robustly
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
            for s in {int(x), int(x) + 1, int(x) - 1, int(round(x)), int(x) + 2, int(x) - 2}:
                if s > 0:
                    candidates_S.add(s)
    except Exception:
        pf = None

    # Try solving 3N^2 - 23N + 45 = S via discriminant check: D = 12S - 11 must be a perfect square
    for S in sorted(candidates_S):
        D = 12 * S - 11
        if D >= 0:
            r = isqrt(D)
            if r * r == D:
                for num in (23 + r, 23 - r):
                    if num % 6 == 0:
                        N = num // 6
                        if N >= 4:
                            if Fraction(1, S_of_N(N)) == f:
                                return N
                            if pf is not None and abs(1.0 / S_of_N(N) - pf) <= 1e-12 * max(1.0, abs(pf)):
                                return N

    # Fallback: local search around approximate N from quadratic formula
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
            S = S_of_N(N)
            if S > 0:
                if Fraction(1, S) == f or abs(1.0 / S - pf) <= 1e-12 * max(1.0, abs(pf)):
                    return N

    # Last resort: monotone search from N=4; p(N) decreases with N for N >= 4
    N = 4
    maxN = 10**6
    while N <= maxN:
        S = S_of_N(N)
        if S > 0:
            g = Fraction(1, S)
            if g == f:
                return N
            if pf is not None and float(g) < pf:
                break
            if pf is None and g < f:
                break
        N += 1

    return None

solve(1/115)

# 调用 solve
result = solve(inputs['p'])
print(result)