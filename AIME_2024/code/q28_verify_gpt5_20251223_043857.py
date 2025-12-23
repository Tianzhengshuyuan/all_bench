inputs = {'ab2': 41}

def solve(ab2):
    from fractions import Fraction
    from math import gcd, isqrt

    def squarefree_part(n):
        s = 1
        left = 1
        d = 2
        nn = n
        while d * d <= nn:
            cnt = 0
            while nn % d == 0:
                nn //= d
                cnt += 1
            if cnt:
                s *= d ** (cnt // 2)
                if cnt % 2 == 1:
                    left *= d
            d += 1 if d == 2 else 2  # after 2, check only odd
        left *= nn
        return s, left

    # Given: AB=CD=sqrt(ab2), AC=BD=sqrt(80), AD=BC=sqrt(89)
    b2 = 80
    c2 = 89

    # u=x1^2, v=x2^2, w=x3^2
    u = Fraction(ab2 + c2 - b2, 2)
    v = Fraction(ab2 + b2 - c2, 2)
    w = Fraction(b2 + c2 - ab2, 2)

    # r = sqrt(u v w) / (2 sqrt(u v + u w + v w))
    a = u * v * w
    b = u * v + u * w + v * w
    ab = a * b  # Fraction

    M = ab.numerator
    N = ab.denominator
    p = b.numerator
    q = b.denominator

    # r = q * sqrt(M/N) / (2p) = q * sqrt(MN) / (2 p N)
    T = M * N
    s, n_sf = squarefree_part(T)
    m = q * s
    p_final = 2 * p * N

    g = gcd(m, p_final)
    m //= g
    p_final //= g

    return m + n_sf + p_final

solve(ab2)

# 调用 solve
result = solve(inputs['ab2'])
print(result)