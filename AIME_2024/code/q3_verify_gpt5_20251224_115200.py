inputs = {'p': '1/115'}

def solve(p):
    from fractions import Fraction
    from math import isqrt

    # Convert input to a rational fraction
    try:
        f = Fraction(p).limit_denominator()
    except Exception:
        f = Fraction(str(p)).limit_denominator()

    if f <= 0:
        return None

    # Try to use the exact reciprocal S = 1/p (and nearby integers to handle float inputs)
    inv = Fraction(1, 1) / f
    candidates_S = set()
    if inv.denominator == 1:
        candidates_S.add(inv.numerator)
    else:
        x = float(inv)
        for s in {int(x), int(x) + 1, int(x) - 1}:
            if s > 0:
                candidates_S.add(s)

    # Quadratic method: 3N^2 - 23N + 45 = S, D = 12S - 11 must be a perfect square
    for S in sorted(candidates_S):
        D = 12 * S - 11
        if D > 0:
            r = isqrt(D)
            if r * r == D:
                for num in (23 + r, 23 - r):
                    if num % 6 == 0:
                        N = num // 6
                        if N >= 4:
                            # Verify against original p for safety
                            S_check = 3 * N * N - 23 * N + 45
                            if S_check == S and Fraction(1, S_check) == f:
                                return N

    # Fallback: monotone search by comparing p(N) = 1 / (3N^2 - 23N + 45)
    N = 4
    while True:
        S = 3 * N * N - 23 * N + 45
        if S > 0:
            g = Fraction(1, S)
            if g == f:
                return N
            # Tolerance check for float-like inputs
            try:
                pf = float(p)
                if abs(float(g) - pf) <= 1e-12 * max(1.0, abs(pf)):
                    return N
            except Exception:
                pass
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