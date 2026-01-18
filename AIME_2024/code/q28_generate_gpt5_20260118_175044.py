inputs = {'ab_sq': 29}

def solve(ab_sq):
    from fractions import Fraction
    import math

    s1 = int(ab_sq)  # AB^2
    s2 = 80          # AC^2 (fixed by problem)
    s3 = 89          # BC^2 (fixed by problem)

    # Using the rectangular prism model:
    # a^2 = (AB^2 + AC^2 - BC^2)/2, etc. We only need S = 2*(1/a^2 + 1/b^2 + 1/c^2)
    d1 = s1 + s2 - s3  # a^2 * 2
    d2 = s1 + s3 - s2  # b^2 * 2
    d3 = s2 + s3 - s1  # c^2 * 2

    # Distance r from center (a/2,b/2,c/2) to plane x/a + y/b + z/c = 1 is r = (1/2)/sqrt(1/a^2+1/b^2+1/c^2)
    # Note that 1/a^2 = 2/d1, etc., so S = 1/a^2+1/b^2+1/c^2 = 2*(1/d1 + 1/d2 + 1/d3)
    S = Fraction(2, 1) * (Fraction(1, d1) + Fraction(1, d2) + Fraction(1, d3))

    # r = 1 / (2*sqrt(S)) = sqrt(B) / (2*sqrt(A)) where S = A/B in lowest terms
    A = S.numerator
    B = S.denominator

    # After rationalizing: r = sqrt(A*B) / (2*A)
    T = A * B

    # Factor T to extract square part: T = c^2 * n with n squarefree
    t = T
    c = 1
    n = 1

    # Factor out 2s
    cnt = 0
    while t % 2 == 0:
        t //= 2
        cnt += 1
    if cnt:
        c *= 2 ** (cnt // 2)
        if cnt % 2 == 1:
            n *= 2

    # Factor odd primes
    f = 3
    while f * f <= t:
        cnt = 0
        while t % f == 0:
            t //= f
            cnt += 1
        if cnt:
            c *= f ** (cnt // 2)
            if cnt % 2 == 1:
                n *= f
        f += 2
    if t > 1:
        n *= t

    m = c
    p = 2 * A
    g = math.gcd(m, p)
    m //= g
    p //= g

    return m + n + p

# 调用 solve
result = solve(inputs['ab_sq'])
print(result)