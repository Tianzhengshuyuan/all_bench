inputs = {'ab_sq': 41}

from fractions import Fraction
from math import gcd, isqrt

def solve(ab_sq):
    # Given opposite edge squares:
    a = ab_sq
    b = 80
    c = 89

    # Solve for x^2, y^2, z^2 where:
    # a = x^2 + y^2, b = y^2 + z^2, c = z^2 + x^2
    X = Fraction(c + a - b, 2)
    Y = Fraction(a + b - c, 2)
    Z = Fraction(b + c - a, 2)

    # r^2 = (XYZ) / (4 * (XY + YZ + ZX))
    num = X * Y * Z
    den = X * Y + Y * Z + Z * X
    R2 = num / (den * 4)

    N = R2.numerator
    D = R2.denominator

    def squarefree_decomp(n):
        # returns (s, r) such that n = s^2 * r, r squarefree
        s = 1
        r = 1
        x = n
        if x == 0:
            return 0, 1
        # factor 2
        cnt = 0
        while x % 2 == 0:
            x //= 2
            cnt += 1
        if cnt // 2:
            s *= 2 ** (cnt // 2)
        if cnt % 2 == 1:
            r *= 2
        p = 3
        while p * p <= x:
            cnt = 0
            while x % p == 0:
                x //= p
                cnt += 1
            if cnt // 2:
                s *= p ** (cnt // 2)
            if cnt % 2 == 1:
                r *= p
            p += 2
        if x > 1:
            # prime factor remains with exponent 1
            r *= x
        return s, r

    # Simplify sqrt(N/D) to form m*sqrt(n)/p
    g = gcd(N, D)
    N //= g
    D //= g

    sN, rN = squarefree_decomp(N)
    sD, rD = squarefree_decomp(D)

    # sqrt(N/D) = (sN/sD) * sqrt(rN/rD) = (sN/(sD*rD)) * sqrt(rN*rD)
    m0 = sN
    p0 = sD * rD
    rad = rN * rD

    sRad, rSqFree = squarefree_decomp(rad)
    m = m0 * sRad
    p = p0

    g2 = gcd(m, p)
    m //= g2
    p //= g2
    n = rSqFree

    # r = sqrt(R2) = m*sqrt(n)/p
    return m + n + p

solve(ab_sq)

# 调用 solve
result = solve(inputs['ab_sq'])
print(result)