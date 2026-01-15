inputs = {'ab_sq': 41}

def solve(ab_sq):
    from fractions import Fraction
    from math import gcd

    def squarefree_split(n):
        n = int(n)
        if n == 0:
            return 0, 0
        if n < 0:
            n = -n
        sf = 1  # squarefree part
        s = 1   # square root of square part
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
        return sf, s

    # Opposite edge squares: AB^2=CD^2=a, AC^2=BD^2=b, AD^2=BC^2=c
    a = int(ab_sq)
    b = 80
    c = 89

    # Disphenoid parameters: x2=4x^2, y2=4y^2, z2=4z^2
    x2 = Fraction(b + c - a, 2)
    y2 = Fraction(a + c - b, 2)
    z2 = Fraction(a + b - c, 2)

    # Inradius squared: r^2 = (x2*y2*z2) / (4*(x2*y2 + x2*z2 + y2*z2))
    A = x2 * y2 * z2
    B = x2 * y2 + x2 * z2 + y2 * z2
    q = A / (4 * B)  # r^2 as a reduced Fraction

    num = q.numerator
    den = q.denominator

    snum, tnum = squarefree_split(num)
    sden, tden = squarefree_split(den)

    # r = (tnum * sqrt(snum*sden)) / (tden * sden)
    m = tnum
    n = snum * sden
    p = tden * sden

    g = gcd(m, p)
    m //= g
    p //= g

    return m + n + p

solve(41)

# 调用 solve
result = solve(inputs['ab_sq'])
print(result)