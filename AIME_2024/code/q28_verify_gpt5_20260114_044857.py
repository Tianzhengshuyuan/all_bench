inputs = {'ab_sq': 41}

def solve(ab_sq):
    from fractions import Fraction
    from math import gcd

    def squarefree_split(n):
        # Return (squarefree_part, sqrt_square_part) where n = squarefree_part * (sqrt_square_part)^2
        n = int(n)
        if n == 0:
            return 0, 0
        if n < 0:
            n = -n
        sf = 1
        root = 1
        x = n

        cnt = 0
        while x % 2 == 0:
            x //= 2
            cnt += 1
        if cnt:
            root *= 2 ** (cnt // 2)
            if cnt % 2:
                sf *= 2

        d = 3
        while d * d <= x:
            cnt = 0
            while x % d == 0:
                x //= d
                cnt += 1
            if cnt:
                root *= d ** (cnt // 2)
                if cnt % 2:
                    sf *= d
            d += 2
        if x > 1:
            sf *= x
        return sf, root

    # Opposite edge squares: AB^2=CD^2=a, AC^2=BD^2=b, AD^2=BC^2=c
    a = int(ab_sq)
    b = 80
    c = 89

    # Disphenoid parameters: x2=4x^2, y2=4y^2, z2=4z^2
    x2 = Fraction(b + c - a, 2)  # = 4x^2
    y2 = Fraction(a + c - b, 2)  # = 4y^2
    z2 = Fraction(a + b - c, 2)  # = 4z^2

    # Inradius squared: r^2 = (x2*y2*z2) / (4*(x2*y2 + x2*z2 + y2*z2))
    A = x2 * y2 * z2
    B = x2 * y2 + x2 * z2 + y2 * z2
    q = A / (4 * B)  # r^2 as Fraction

    num = q.numerator
    den = q.denominator

    snum, rnum = squarefree_split(num)
    sden, rden = squarefree_split(den)

    # r = (rnum * sqrt(snum*sden)) / (rden * sden)
    m = rnum
    n = snum * sden
    p = rden * sden

    g = gcd(m, p)
    m //= g
    p //= g

    return m + n + p

solve(41)

# 调用 solve
result = solve(inputs['ab_sq'])
print(result)