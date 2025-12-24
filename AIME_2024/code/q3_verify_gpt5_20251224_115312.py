inputs = {'p': '1/115'}

def solve(p):
    from fractions import Fraction
    from math import isqrt

    # Convert p to a fraction; keep it rational if possible
    try:
        f = Fraction(p).limit_denominator()
    except Exception:
        f = Fraction(str(p)).limit_denominator()

    if f <= 0:
        return None

    # Monotone search using p(N) = 1 / (3N^2 - 23N + 45)
    # p(N) decreases with N for N >= 4
    N = 4
    try:
        pf = float(p)
    except Exception:
        pf = None

    while True:
        S = 3 * N * N - 23 * N + 45
        if S > 0:
            g = Fraction(1, S)
            if g == f:
                return N
            if pf is not None and abs(float(g) - pf) <= 1e-12 * max(1.0, abs(pf)):
                return N
            if g < f:
                break
        N += 1
        if N > 10**7:
            break

    # Algebraic solve if 1/p is (close to) an integer
    inv = Fraction(1, 1) / f
    if inv.denominator == 1:
        S = inv.numerator
        D = 12 * S - 11
        if D >= 0:
            r = isqrt(D)
            if r * r == D:
                for num in (23 + r, 23 - r):
                    if num % 6 == 0:
                        N = num // 6
                        if N >= 4 and (3 * N * N - 23 * N + 45) == S:
                            return N

    return None

solve(1/115)

# 调用 solve
result = solve(inputs['p'])
print(result)