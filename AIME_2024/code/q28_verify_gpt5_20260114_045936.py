inputs = {'ab_sq': 41}

def solve(ab_sq):
    from fractions import Fraction
    from math import gcd

    def square_decompose(n):
        # Return (s, f) with n = s^2 * f and f squarefree
        n = int(n)
        if n == 0:
            return 0, 0
        if n < 0:
            n = -n
        s = 1
        f = 1
        d = 2
        while d * d <= n:
            cnt = 0
            while n % d == 0:
                n //= d
                cnt += 1
            if cnt:
                s *= d ** (cnt // 2)
                if cnt % 2:
                    f *= d
            d = 3 if d == 2 else d + 2
        if n > 1:
            f *= n
        return s, f

    a = int(ab_sq)  # AB^2 = CD^2
    b = 80          # AC^2 = BD^2
    c = 89          # AD^2 = BC^2

    # Disphenoid relations with x2=4x^2, etc.
    x2 = Fraction(b + c - a, 2)
    y2 = Fraction(a + c - b, 2)
    z2 = Fraction(a + b - c, 2)

    # r^2 = (x2*y2*z2) / (4*(x2*y2 + x2*z2 + y2*z2))
    A = x2 * y2 * z2
    B = x2 * y2 + x2 * z2 + y2 * z2
    q = A / (4 * B)

    num = q.numerator
    den = q.denominator

    sN, fN = square_decompose(num)
    sD, fD = square_decompose(den)

    # Remove common factors from squarefree parts to keep n squarefree
    gsf = gcd(fN, fD)
    if gsf > 1:
        fN //= gsf
        fD //= gsf

    # r = (sN/sD) * sqrt(fN/fD) = (sN * sqrt(fN*fD)) / (sD * fD)
    m0 = sN
    p0 = sD * fD
    n = fN * fD

    g = gcd(m0, p0)
    m = m0 // g
    p = p0 // g

    return m + n + p

solve(41)

# 调用 solve
result = solve(inputs['ab_sq'])
print(result)