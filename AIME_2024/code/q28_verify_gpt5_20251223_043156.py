inputs = {'ab2': 41}

from fractions import Fraction
from math import gcd

def solve(ab2):
    # Given: AB^2 = ab2, AC^2 = 80, AD^2 = 89 (opposite edges equal)
    s1 = ab2
    s2 = 80
    s3 = 89

    # Recover a^2, b^2, c^2 from pairwise sums
    x = Fraction(s1 + s3 - s2, 2)  # a^2
    y = Fraction(s1 + s2 - s3, 2)  # b^2
    z = Fraction(s2 + s3 - s1, 2)  # c^2

    # r = (1/2) * sqrt( (xyz)/(xy + yz + zx) )
    num = x * y * z
    den = x * y + y * z + z * x
    Q = Fraction(num, den)  # inside the sqrt

    num_i = Q.numerator
    den_i = Q.denominator

    def square_free_decompose(n):
        if n == 0:
            return 0, 1
        sq = 1
        sf = 1
        d = 2
        temp = n
        while d * d <= temp:
            cnt = 0
            while temp % d == 0:
                temp //= d
                cnt += 1
            if cnt:
                sq *= d ** (cnt // 2)
                if cnt % 2 == 1:
                    sf *= d
            d += 1
        if temp > 1:
            sf *= temp
        return sq, sf

    # sqrt(num_i/den_i) -> m0*sqrt(n0)/p0
    sq1, sf1 = square_free_decompose(num_i)
    sq2, sf2 = square_free_decompose(den_i)

    m0 = sq1
    p0 = sq2 * sf2
    # sqrt(sf1/sf2) = sqrt(sf1*sf2)/sf2; incorporate square parts again
    sq_extra, n0 = square_free_decompose(sf1 * sf2)
    m0 *= sq_extra

    g = gcd(m0, p0)
    m0 //= g
    p0 //= g

    # r = (1/2) * m0*sqrt(n0)/p0
    m = m0
    n = n0
    p = p0 * 2
    g2 = gcd(m, p)
    m //= g2
    p //= g2

    return m + n + p

solve(ab2)

# 调用 solve
result = solve(inputs['ab2'])
print(result)