inputs = {'ab_sq': 41}

def solve(ab_sq):
    from fractions import Fraction
    from math import gcd

    # Given opposite edge squares
    L1 = Fraction(int(ab_sq), 1)  # AB^2 = CD^2 = ab_sq
    L2 = Fraction(80, 1)          # AC^2 = BD^2
    L3 = Fraction(89, 1)          # AD^2 = BC^2

    # Using disphenoid coordinates:
    # 4(a^2 + b^2) = L3, 4(a^2 + c^2) = L2, 4(b^2 + c^2) = L1
    s1 = L1 / 4  # b^2 + c^2
    s2 = L2 / 4  # a^2 + c^2
    s3 = L3 / 4  # a^2 + b^2

    a2 = (s2 + s3 - s1) / 2
    b2 = (s1 + s3 - s2) / 2
    c2 = (s1 + s2 - s3) / 2

    # Inradius r satisfies: r = 1 / sqrt(1/a^2 + 1/b^2 + 1/c^2)
    denom = Fraction(1, 1) / a2 + Fraction(1, 1) / b2 + Fraction(1, 1) / c2  # = pnum/pden
    pnum = denom.numerator
    pden = denom.denominator

    # r = sqrt(pden/pnum) = sqrt(pden*pnum) / pnum
    P = pden * pnum  # integer

    def square_factor(n):
        s = 1
        sf = 1
        d = 2
        while d * d <= n:
            cnt = 0
            while n % d == 0:
                n //= d
                cnt += 1
            if cnt:
                s *= d ** (cnt // 2)
                if cnt % 2:
                    sf *= d
            d = 3 if d == 2 else d + 2
        if n > 1:
            sf *= n
        return s, sf

    s, n_sf = square_factor(P)

    # r = (s * sqrt(n_sf)) / pnum; reduce common factor between s and pnum
    g = gcd(s, pnum)
    m = s // g
    p = pnum // g
    n = n_sf

    return m + n + p

solve(41)

# 调用 solve
result = solve(inputs['ab_sq'])
print(result)