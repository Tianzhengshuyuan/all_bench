inputs = {'p': '1/115'}

def solve(p):
    from fractions import Fraction
    from math import isqrt

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

    # Try algebraic solution using S = 1/p
    inv = Fraction(1, 1) / f
    candidates_S = set()
    if inv.denominator == 1 and inv.numerator > 0:
        candidates_S.add(inv.numerator)

    # Handle float inputs by considering nearby integers
    try:
        x = float(inv)
        for s in {int(x), int(x) + 1, int(x) - 1, int(round(x))}:
            if s > 0:
                candidates_S.add(s)
    except Exception:
        pass

    for S in sorted(candidates_S):
        D = 12 * S - 11
        if D >= 0:
            r = isqrt(D)
            if r * r == D:
                for num in (23 + r, 23 - r):
                    if num % 6 == 0:
                        N = num // 6
                        if N >= 4 and p_of_N(N) == f:
                            return N

    # Fallback: monotone search since p(N) = 1 / (3N^2 - 23N + 45) decreases for N >= 4
    try:
        pf = float(p)
    except Exception:
        pf = None

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
        if pf is not None and abs(float(g) - pf) <= 1e-12 * max(1.0, abs(pf)):
            return N
        if g < f:
            break
        N += 1
        if N > 10**6:
            break

    return None

solve(1/115)

# 调用 solve
result = solve(inputs['p'])
print(result)