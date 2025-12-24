inputs = {'p': '1/115'}

def solve(p):
    from fractions import Fraction
    from math import isqrt

    # Convert p to a fraction; try to keep it rational if possible
    try:
        f = Fraction(p).limit_denominator()
    except Exception:
        f = Fraction(str(p)).limit_denominator()

    # We know p = 1 / S(N) with S(N) integer; try to extract integer S
    inv = Fraction(1, 1) / f
    if inv.denominator == 1:
        S = inv.numerator
    else:
        # Fallback for float inputs: approximate S by rounding
        S = int(round(float(inv)))

    # Solve 3N^2 - 23N + 45 = S  -> Discriminant D = 12*S - 11 must be a perfect square
    D = 12 * S - 11
    r = isqrt(D)

    # If not perfect square, adjust S slightly (handles rounding from float inputs)
    if r * r != D:
        found = False
        for delta in range(-10, 11):
            if S + delta > 0:
                D2 = 12 * (S + delta) - 11
                r2 = isqrt(D2)
                if r2 * r2 == D2:
                    S += delta
                    D = D2
                    r = r2
                    found = True
                    break
        if not found:
            return None

    # Roots: N = (23 ± r) / 6; pick integer root >= 4 that satisfies the equation
    for num in (23 + r, 23 - r):
        if num % 6 == 0:
            N = num // 6
            if N >= 4 and (3 * N * N - 23 * N + 45) == S:
                return N

    # Final fallback: small local search
    for N in range(4, 10000):
        if (3 * N * N - 23 * N + 45) == S:
            return N
        if (3 * N * N - 23 * N + 45) > S and N > 4:
            break

    return None

solve(1/115)

# 调用 solve
result = solve(inputs['p'])
print(result)