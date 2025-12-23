inputs = {'ab2': 41}

def solve(ab2):
    from fractions import Fraction
    from math import gcd

    def factorize(n):
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

    # Given opposite edge squares: ab2, 80, 89
    L = [ab2, 80, 89]

    # Recover p^2, q^2, r^2 (in some order), using:
    # p^2 = (L1 + L2 - L3)/2 etc.
    X = Fraction(L[0] + L[1] - L[2], 2)
    Y = Fraction(L[0] + L[2] - L[1], 2)
    Z = Fraction(L[1] + L[2] - L[0], 2)

    # r^2 = (XYZ)/(XY + XZ + YZ) and r = (1/2) * sqrt(r^2)
    R = (X * Y * Z) / (X * Y + X * Z + Y * Z)
    a = R.numerator
    b = R.denominator

    # Decompose a and b into square parts
    sqa, a_rest = square_part_and_rest(a)
    sqb, b_rest = square_part_and_rest(b)

    # r = (sqa / (2*sqb)) * sqrt(a_rest / b_rest)
    # => r = (sqa * sqrt(a_rest * b_rest)) / (2 * sqb * b_rest)
    n = a_rest * b_rest
    m0 = sqa
    p0 = 2 * sqb * b_rest

    g = gcd(m0, p0)
    m = m0 // g
    p = p0 // g

    return m + n + p

solve(41)

# 调用 solve
result = solve(inputs['ab2'])
print(result)