inputs = {'p': '1/115'}

def solve(p):
    from fractions import Fraction
    import math

    # Normalize p to a Fraction for robustness
    try:
        pf = Fraction(p).limit_denominator(10**9)
    except TypeError:
        pf = Fraction(str(p)).limit_denominator(10**9)

    if pf == 0:
        return None

    # For this setup, p = 1 / (3N^2 - 23N + 45) = 1 / D
    if pf.numerator == 1:
        D = pf.denominator
    else:
        # Fallback if p not exactly 1/D in given type
        D = round(float(1 / pf))

    # Solve 3N^2 - 23N + 45 = D  =>  3N^2 - 23N + (45 - D) = 0
    # Discriminant: Δ = 23^2 - 4*3*(45 - D) = 12D - 11
    def try_from_D(dd):
        if dd <= 0:
            return None
        disc = 12 * dd - 11
        if disc < 0:
            return None
        s = math.isqrt(disc)
        if s * s != disc:
            return None
        for sign in (1, -1):
            num = 23 + sign * s
            if num % 6 == 0:
                N = num // 6
                if N >= 4:
                    denom = 3 * N * N - 23 * N + 45
                    # Verify matches p exactly (fraction) or numerically (float)
                    if Fraction(1, denom) == pf or abs(1.0 / denom - float(pf)) < 1e-12:
                        return N
        return None

    # Try the main candidate D and a small neighborhood for robustness
    for delta in (0, -1, 1, -2, 2, -3, 3):
        ans = try_from_D(D + delta)
        if ans is not None:
            return ans

    # As a last resort, brute force in a window around sqrt(D/3)
    approxN = int(max(4, math.sqrt(max(1, D) / 3)))
    for N in range(max(4, approxN - 10000), approxN + 10001):
        denom = 3 * N * N - 23 * N + 45
        if denom > 0 and (Fraction(1, denom) == pf or abs(1.0 / denom - float(pf)) < 1e-12):
            return N

    return None

solve(p)

# 调用 solve
result = solve(inputs['p'])
print(result)