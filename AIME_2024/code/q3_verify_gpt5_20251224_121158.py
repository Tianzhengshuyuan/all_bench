inputs = {'p': '1/115'}

def solve(p):
    from fractions import Fraction
    from math import isqrt

    # Normalize p to a Fraction
    try:
        pf = Fraction(p).limit_denominator(10**12)
    except Exception:
        pf = Fraction(str(p)).limit_denominator(10**12)

    if pf <= 0 or pf > 1:
        return None

    # For this problem, p(N) = 1 / (3(N-4)^2 + (N-4) + 1) = 1 / (3N^2 - 23N + 45)
    # Let S = 1/p, and we need S = 3x^2 + x + 1 with x = N - 4 (x >= 0 integer)
    # Discriminant condition: 12S - 11 must be a perfect square, and (sqrt(12S-11) - 1) % 6 == 0

    def try_S(S, target_frac, target_float=None):
        if S <= 0:
            return None
        disc = 12 * S - 11
        if disc < 0:
            return None
        s = isqrt(disc)
        if s * s != disc:
            return None
        if (s - 1) % 6 != 0:
            return None
        x = (s - 1) // 6
        if x < 0:
            return None
        N = x + 4
        denom = 3 * N * N - 23 * N + 45
        if denom <= 0:
            return None
        if Fraction(1, denom) == target_frac:
            return N
        if target_float is not None and abs(1.0 / denom - target_float) <= 1e-12 * max(1.0, abs(target_float)):
            return N
        return None

    # Exact S if p is a unit fraction
    inv = Fraction(1, 1) / pf
    candidates_S = set()
    if inv.denominator == 1:
        candidates_S.add(inv.numerator)

    # Include candidates from float approximation
    try:
        p_float = float(pf)
        if p_float > 0:
            D_guess = int(round(1.0 / p_float))
            for delta in range(-5, 6):
                if D_guess + delta > 0:
                    candidates_S.add(D_guess + delta)
    except Exception:
        p_float = None

    for S in sorted(candidates_S):
        ans = try_S(S, pf, p_float if 'p_float' in locals() else None)
        if ans is not None:
            return ans

    # Fallback: monotone search in N (p(N) decreases for N >= 4)
    def p_of_N(N):
        D = 3 * N * N - 23 * N + 45
        if D <= 0:
            return None
        return Fraction(1, D)

    N = 4
    maxN = 10**6
    while N <= maxN:
        g = p_of_N(N)
        if g is None:
            N += 1
            continue
        if g == pf:
            return N
        if p_float is not None:
            if abs(float(g) - p_float) <= 1e-12 * max(1.0, abs(p_float)):
                return N
            if float(g) < p_float:
                break
        else:
            if g < pf:
                break
        N += 1

    return None

solve(1/115)

# 调用 solve
result = solve(inputs['p'])
print(result)