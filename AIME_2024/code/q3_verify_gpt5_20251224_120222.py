inputs = {'p': '1/115'}

def solve(p):
    from fractions import Fraction
    from math import isqrt

    try:
        f = Fraction(p).limit_denominator(10**9)
    except Exception:
        f = Fraction(str(p)).limit_denominator(10**9)

    if f <= 0 or f > 1:
        return None

    def S_of_N(N):
        return 3 * N * N - 23 * N + 45

    def p_of_N(N):
        s = S_of_N(N)
        if s <= 0:
            return None
        return Fraction(1, s)

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

    inv = Fraction(1, 1) / f
    candidates_S = set()
    if inv.denominator == 1 and inv.numerator > 0:
        candidates_S.add(inv.numerator)
    if pf is not None and pf > 0:
        x = 1.0 / pf
        for s in {int(x), int(x) + 1, int(x) - 1, int(round(x))}:
            if s > 0:
                candidates_S.add(s)

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