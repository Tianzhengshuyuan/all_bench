inputs = {'ab_sq': 41}

from fractions import Fraction
from math import gcd, isqrt

def solve(ab_sq):
    x2 = Fraction(ab_sq)
    y2 = Fraction(80)
    z2 = Fraction(89)

    a2 = (x2 + z2 - y2) / 2
    b2 = (x2 + y2 - z2) / 2
    c2 = (y2 + z2 - x2) / 2

    A = a2 * b2 * c2
    B = a2 * b2 + b2 * c2 + c2 * a2

    R2 = A / B
    num = R2.numerator
    den = R2.denominator

    M = num * den

    def squarefree_decomp(n):
        q = 1
        n_sf = 1
        d = 2
        while d * d <= n:
            exp = 0
            while n % d == 0:
                n //= d
                exp += 1
            if exp:
                q *= d ** (exp // 2)
                if exp % 2 == 1:
                    n_sf *= d
            d = 3 if d == 2 else d + 2
        if n > 1:
            n_sf *= n
        return q, n_sf

    q, n_sf = squarefree_decomp(M)
    p = 2 * den
    g = gcd(q, p)
    m = q // g
    p //= g
    return m + n_sf + p

solve(41)

# 调用 solve
result = solve(inputs['ab_sq'])
print(result)