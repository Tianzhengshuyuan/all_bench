inputs = {'p': '1/115'}

def solve(p):
    from fractions import Fraction
    from math import isqrt

    # Convert input to a rational fraction
    try:
        f = Fraction(p).limit_denominator()
    except Exception:
        f = Fraction(str(p)).limit_denominator()

    if f <= 0 or f > 1:
        return None

    def S_of_N(N):
        return 3 * N * N - 23 * N + 45

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
                            g = Fraction(1, S)
                            if g == f:
                                return N
                            if pf is not None and abs(float(g) - pf) <= 1e-12 * max(1.0, abs(pf)):
                                return N

    # Fallback: monotone search since p(N) decreases for N >= 4
    N = 4
    limit = 10**6
    while N <= limit:
        S = S_of_N(N)
        if S > 0:
            g = Fraction(1, S)
            if g == f:
                return N
            if pf is not None:
                if abs(float(g) - pf) <= 1e-12 * max(1.0, abs(pf)):
                    return N
                if float(g) < pf:
                    break
            else:
                if inv.denominator == 1 and S > inv.numerator:
                    break
        N += 1

    return None

solve(1/115)

# 调用 solve
result = solve(inputs['p'])
print(result)