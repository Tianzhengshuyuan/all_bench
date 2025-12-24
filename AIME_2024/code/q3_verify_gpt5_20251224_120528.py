inputs = {'p': '1/115'}

def solve(p):
    from fractions import Fraction
    from math import isqrt
    import math

    def to_fraction(x):
        from fractions import Fraction as F
        if isinstance(x, F):
            return x
        if isinstance(x, int):
            return F(x, 1)
        if isinstance(x, float):
            return F(x).limit_denominator(10**9)
        if isinstance(x, str):
            try:
                return F(x)
            except Exception:
                return F(float(x)).limit_denominator(10**9)
        try:
            return F(x)
        except Exception:
            return F(float(x)).limit_denominator(10**9)

    p_frac = to_fraction(p)
    if p_frac <= 0:
        return None

    Dval = Fraction(1, 1) / p_frac
    disc = -11 + 12 * Dval  # discriminant

    # Exact integer approach
    if disc.denominator == 1:
        dnum = disc.numerator
        if dnum >= 0:
            s = isqrt(dnum)
            if s * s == dnum:
                for num in (23 + s, 23 - s):
                    if num % 6 == 0:
                        N = num // 6
                        if N >= 4:
                            den = 3 * N * N - 23 * N + 45
                            if Fraction(1, den) == p_frac:
                                return N

    # Fallback numeric search near approximate solution
    pf = float(p_frac.numerator) / float(p_frac.denominator)
    if pf <= 0:
        return None
    approx_disc = -11.0 + 12.0 / pf
    approx_disc = max(0.0, approx_disc)
    approx_s = math.sqrt(approx_disc)
    Napprox = (23.0 + approx_s) / 6.0
    start = max(4, int(math.floor(Napprox)) - 100)
    end = int(math.ceil(Napprox)) + 100
    for N in range(start, end + 1):
        den = 3 * N * N - 23 * N + 45
        if den > 0 and Fraction(1, den) == p_frac:
            return N

    return None

solve(p)

# 调用 solve
result = solve(inputs['p'])
print(result)