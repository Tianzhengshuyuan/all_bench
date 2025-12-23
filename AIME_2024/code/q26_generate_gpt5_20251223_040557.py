inputs = {'BC': 5}

def solve(BC):
    from fractions import Fraction
    from math import isqrt, sqrt

    AB = 5
    AC = 10

    # Using AP = 2*AB*AC / sqrt(2*AB^2 + 2*AC^2 - BC^2)
    twoABAC = 2 * AB * AC  # 100
    BCf = Fraction(BC).limit_denominator()
    Nf = Fraction(2 * AB * AB + 2 * AC * AC, 1) - BCf * BCf  # 250 - BC^2

    # Try exact rational sqrt
    p, q = Nf.numerator, Nf.denominator
    sp, sq = isqrt(p), isqrt(q)
    if p > 0 and q > 0 and sp * sp == p and sq * sq == q:
        num = twoABAC * sq
        den = sp
        # gcd
        a, b = abs(num), abs(den)
        while b:
            a, b = b, a % b
        g = a
        m = num // g
        n = den // g
        return m + n

    # Fallback (unlikely used for given test), return rounded m+n from best rational approx
    AP = twoABAC / sqrt(float(Nf))
    from fractions import Fraction as Fr
    frac = Fr(AP).limit_denominator(10**6)
    return frac.numerator + frac.denominator

solve(9)

# 调用 solve
result = solve(inputs['BC'])
print(result)