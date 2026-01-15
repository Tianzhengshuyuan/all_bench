inputs = {'ab_sq': 41}

def solve(ab_sq):
    from fractions import Fraction
    import math

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

        p = 3
        while p * p <= x:
            cnt = 0
            while x % p == 0:
                x //= p
                cnt += 1
            if cnt:
                root *= p ** (cnt // 2)
                if cnt % 2 == 1:
                    sf *= p
            p += 2
        if x > 1:
            sf *= x
        return sf, root

    # Given constants from the problem
    b = 80  # AC^2 = BD^2
    c = 89  # AD^2 = BC^2
    a = ab_sq  # AB^2 = CD^2

    # Solve for x^2, y^2, z^2 using:
    # x^2 = (a + b - c)/2, y^2 = (a + c - b)/2, z^2 = (b + c - a)/2
    x2 = Fraction(a + b - c, 2)
    y2 = Fraction(a + c - b, 2)
    z2 = Fraction(b + c - a, 2)

    # r^2 = (x2*y2*z2) / (4*(x2*y2 + x2*z2 + y2*z2))
    A = x2 * y2 * z2
    B = x2 * y2 + x2 * z2 + y2 * z2
    q = A / (4 * B)  # r^2 as Fraction

    if q < 0:
        q = -q  # safeguard, though in the intended domain r^2 > 0

    num = q.numerator
    den = q.denominator

    snum, tnum = squarefree_split(num)
    sden, tden = squarefree_split(den)

    n = snum * sden  # squarefree
    m = tnum
    p = tden * sden

    g = math.gcd(m, p)
    if g > 1:
        m //= g
        p //= g

    return m + n + p

solve(ab_sq)

# 调用 solve
result = solve(inputs['ab_sq'])
print(result)