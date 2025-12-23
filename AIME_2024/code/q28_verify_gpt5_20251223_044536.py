inputs = {'ab2': 41}

def solve(ab2):
    from fractions import Fraction
    from math import gcd, isqrt

    def squarefree_decompose(n):
        n = abs(int(n))
        s = 1
        t = 1
        i = 2
        while i * i <= n:
            e = 0
            while n % i == 0:
                n //= i
                e += 1
            if e:
                s *= i ** (e // 2)
                if e % 2 == 1:
                    t *= i
            i = 3 if i == 2 else i + 2
        if n > 1:
            t *= n
        return s, t

    # Given constants from the problem
    ac2 = 80
    ad2 = 89

    # Compute x^2, y^2, z^2 from the system:
    # x^2 + y^2 = ab2
    # x^2 + z^2 = ac2
    # y^2 + z^2 = ad2
    x2 = Fraction(ab2 + ac2 - ad2, 2)
    y2 = Fraction(ab2 + ad2 - ac2, 2)
    z2 = Fraction(ac2 + ad2 - ab2, 2)

    # r^2 = (x2*y2*z2) / (4*(x2*y2 + y2*z2 + z2*x2))
    num = x2 * y2 * z2
    den = x2 * y2 + y2 * z2 + z2 * x2
    r2 = num / (4 * den)

    a = r2.numerator
    b = r2.denominator

    sa, ta = squarefree_decompose(a)
    sb, tb = squarefree_decompose(b)

    m = sa
    n = ta * tb
    p = sb * tb

    g = gcd(m, p)
    m //= g
    p //= g

    return m + n + p

solve(41)

# 调用 solve
result = solve(inputs['ab2'])
print(result)