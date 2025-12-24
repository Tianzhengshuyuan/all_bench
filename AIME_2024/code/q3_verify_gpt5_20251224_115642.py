inputs = {'p': '1/115'}

from fractions import Fraction
from math import isqrt

def solve(p):
    # Convert p to exact Fraction
    try:
        p_frac = Fraction(p)
    except Exception:
        p_frac = Fraction(str(p))
    if p_frac <= 0:
        return None

    # Target S(N) = 1/p
    T = Fraction(1, 1) / p_frac

    # Closed-form using discriminant: S(N) = 3N^2 - 23N + 45 = T
    # D = 12*T - 11 must be a perfect square, and N = (23 + sqrt(D))/6 (integer, >= 4)
    def check_and_return(T_int):
        D = 12 * T_int - 11
        if D < 0:
            return None
        s = isqrt(D)
        if s * s != D:
            return None
        # Check both roots just in case
        candidates = []
        if (23 + s) % 6 == 0:
            candidates.append((23 + s) // 6)
        if (23 - s) % 6 == 0:
            candidates.append((23 - s) // 6)
        for N in candidates:
            if N >= 4 and Fraction(1, 3*N*N - 23*N + 45) == p_frac:
                return N
        return None

    if T.denominator == 1:
        ans = check_and_return(T.numerator)
        if ans is not None:
            return ans

    # Fallback: small brute-force search if p was given imprecisely
    # S(N) grows ~3N^2, so for reasonable p this will be quick
    # Try a reasonable range
    for N in range(4, 200000):
        if Fraction(1, 3*N*N - 23*N + 45) == p_frac:
            return N
    return None

solve(p)

# 调用 solve
result = solve(inputs['p'])
print(result)