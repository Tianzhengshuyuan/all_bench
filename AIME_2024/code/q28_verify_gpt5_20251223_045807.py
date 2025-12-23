inputs = {'ab2': 41}

from fractions import Fraction
from math import gcd

def solve(ab2):
    def factorize(n):
        n = abs(n)
        f = {}
        d = 2
        while d * d <= n:
            while n % d == 0:
                f[d] = f.get(d, 0) + 1
                n //= d
            d = 3 if d == 2 else d + 2
        if n > 1:
            f[n] = f.get(n, 0) + 1
        return f

    def square_part_and_rest(n):
        if n == 0:
            return 0, 1
        f = factorize(n)
        sq = 1
        rest = 1
        for p, e in f.items():
            sq *= p ** (e // 2)
            if e % 2 == 1:
                rest *= p
        return sq, rest

    # Opposite edge squares (given by problem)
    A = ab2       # AB^2 = CD^2
    B = 80        # AC^2 = BD^2
    C = 89        # AD^2 = BC^2

    # x^2, y^2, z^2 in the isosceles disphenoid model:
    # A = 4(x^2 + y^2), B = 4(x^2 + z^2), C = 4(y^2 + z^2)
    X = Fraction(B + C - A, 8)
    Y = Fraction(C + A - B, 8)
    Z = Fraction(A + B - C, 8)

    # Inradius squared: r^2 = (X Y Z) / (X Y + X Z + Y Z)
    num = X * Y * Z
    den = X * Y + X * Z + Y * Z
    if num == 0:
        return 0

    R2 = num / den
    a = R2.numerator
    b = R2.denominator

    # Decompose numerator and denominator into square and squarefree parts
    sqa, a_rest = square_part_and_rest(a)
    sqb, b_rest = square_part_and_rest(b)

    # r = sqrt(a/b) = (sqa/sqb) * sqrt(a_rest/b_rest)
    #   = (sqa * sqrt(a_rest*b_rest)) / (sqb * b_rest)
    n_val = a_rest * b_rest
    sqn, n_sf = square_part_and_rest(n_val)
    m0 = sqa * sqn
    p0 = sqb * b_rest

    # Reduce rational factor
    g = gcd(m0, p0)
    m = m0 // g
    p = p0 // g

    return m + n_sf + p

solve(41)

# 调用 solve
result = solve(inputs['ab2'])
print(result)