inputs = {'p': '1/115'}

def solve(p):
    from fractions import Fraction
    from math import isqrt

    # Normalize p to a rational number
    try:
        pf = Fraction(p).limit_denominator(10**12)
    except Exception:
        pf = Fraction(str(p)).limit_denominator(10**12)

    if pf <= 0 or pf > 1:
        return None

    # Denominator form for conditional probability:
    # p(N) = 1 / (3(N-4)^2 + (N-4) + 1) = 1 / (3N^2 - 23N + 45)
    # Let x = N - 4, then p = 1 / (3x^2 + x + 1)
    # Solve 3x^2 + x + 1 = D where D = 1/p. Discriminant Δ = 12D - 11 must be a perfect square.
    def try_with_D(D, target_frac, target_float=None):
        if D <= 0:
            return None
        disc = 12 * D - 11
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
        # Verify against exact fraction or float (if provided)
        if Fraction(1, denom) == target_frac:
            return N
        if target_float is not None and abs(1.0 / denom - target_float) <= 1e-12 * max(1.0, abs(target_float)):
            return N
        return None

    # Exact candidate D if p is a unit fraction
    if pf.numerator == 1:
        D0 = pf.denominator
        ans = try_with_D(D0, pf)
        if ans is not None:
            return ans

    # Approximate D from float and check nearby integers for robustness
    try:
        p_float = float(pf)
        if p_float > 0:
            D_guess = int(round(1.0 / p_float))
            for delta in range(-5, 6):
                if D_guess + delta > 0:
                    ans = try_with_D(D_guess + delta, pf, p_float)
                    if ans is not None:
                        return ans
    except Exception:
        p_float = None

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