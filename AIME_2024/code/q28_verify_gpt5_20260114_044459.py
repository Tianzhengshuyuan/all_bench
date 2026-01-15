inputs = {'ab_sq': 41}

def solve(ab_sq):
    from fractions import Fraction
    from math import gcd

    def squarefree_split(n):
        # Return (squarefree_part, sqrt_square_part) where n = squarefree_part * (sqrt_square_part)^2
        if n == 0:
            return 0, 0
        if n < 0:
            n = -n
        sf = 1
        root = 1
        x = n

        # factor 2
        cnt = 0
        while x % 2 == 0:
            x //= 2
            cnt += 1
        if cnt:
            root *= 2 ** (cnt // 2)
            if cnt % 2 == 1:
                sf *= 2

        d = 3
        while d * d <= x:
            cnt = 0
            while x % d == 0:
                x //= d
                cnt += 1
            if cnt:
                root *= d ** (cnt // 2)
                if cnt % 2 == 1:
                    sf *= d
            d += 2
        if x > 1:
            sf *= x
        return sf, root

    # Opposite edge squares: AB^2=CD^2=a, AC^2=BD^2=b, AD^2=BC^2=c
    a = int(ab_sq)
    b = 80
    c = 89

    # Using disphenoid relations with x2=4*x^2 etc. (any permutation works due to symmetry)
    x2 = Fraction(a + b - c, 2)
    y2 = Fraction(a + c - b, 2)
    z2 = Fraction(b + c - a, 2)

    # r^2 = (x2*y2*z2) / (4*(x2*y2 + x2*z2 + y2*z2))
    A = x2 * y2 * z2
    B = x2 * y2 + x2 * z2 + y2 * z2
    q = A / (4 * B)  # r^2 as Fraction

    num = q.numerator
    den = q.denominator

    # Factor numerator and denominator into squarefree and square parts
    snum, tnum = squarefree_split(num)
    sden, tden = squarefree_split(den)

    # r = (tnum * sqrt(snum*sden)) / (tden * sden)
    n = snum * sden
    m = tnum
    p = tden * sden

    g = gcd(m, p)
    if g > 1:
        m //= g
        p //= g

    return m + n + p

solve(41)

# 调用 solve
result = solve(inputs['ab_sq'])
print(result)