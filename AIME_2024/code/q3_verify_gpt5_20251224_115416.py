inputs = {'p': '1/115'}

def solve(p):
    from fractions import Fraction
    from math import isqrt, sqrt

    # Convert p to a fraction
    try:
        f = Fraction(p).limit_denominator()
    except Exception:
        f = Fraction(str(p)).limit_denominator()

    if f <= 0 or f > 1:
        return None

    def S_of_N(N):
        return 3 * N * N - 23 * N + 45

    def p_of_N(N):
        S = S_of_N(N)
        if S <= 0:
            return None
        return Fraction(1, S)

    # Build candidate S values near 1/p
    candidates_S = set()
    inv = Fraction(1, 1) / f
    if inv.denominator == 1 and inv.numerator > 0:
        candidates_S.add(inv.numerator)

    # Include approximations for float inputs
    try:
        pf = float(p)
        if pf > 0:
            x = 1.0 / pf
            for s in {int(x), int(x) + 1, int(x) - 1, int(round(x))}:
                if s > 0:
                    candidates_S.add(s)
    except Exception:
        pf = None

    # Try solving quadratic 3N^2 - 23N + 45 = S for each candidate S
    for S in sorted(candidates_S):
        D = 12 * S - 11
        if D >= 0:
            r = isqrt(D)
            if r * r == D:
                for num in (23 + r, 23 - r):
                    if num % 6 == 0:
                        N = num // 6
                        if N >= 4 and S_of_N(N) == S:
                            g = p_of_N(N)
                            if g == f:
                                return N
                            if pf is not None and abs(float(g) - pf) <= 1e-12 * max(1.0, abs(pf)):
                                return N

    # Fallback: local search around approximate solution
    if pf is not None and pf > 0:
        S_est = 1.0 / pf
        disc_est = max(0.0, 12.0 * S_est - 11.0)
        N_est = int(round((23.0 + sqrt(disc_est)) / 6.0)) if disc_est >= 0 else 4
        low = max(4, N_est - 2000)
        high = max(low, N_est + 2000)
        for N in range(low, high + 1):
            g = p_of_N(N)
            if g is None:
                continue
            if g == f:
                return N
            if abs(float(g) - pf) <= 1e-12 * max(1.0, abs(pf)):
                return N

    # Last resort: monotone increasing search from N=4, stop once g < f (since p(N) decreases)
    N = 4
    while True:
        g = p_of_N(N)
        if g is None:
            N += 1
            if N > 10**6:
                break
            continue
        if g == f:
            return N
        if pf is not None:
            if abs(float(g) - pf) <= 1e-12 * max(1.0, abs(pf)):
                return N
            if float(g) < float(f):
                break
        else:
            # Without float comparison, stop if S grows too large relative to 1/f
            S_target = inv.numerator // inv.denominator if inv > 0 else None
            if S_target is not None and S_of_N(N) > S_target + 10:
                break
        N += 1
        if N > 10**6:
            break

    return None

solve(1/115)

# 调用 solve
result = solve(inputs['p'])
print(result)