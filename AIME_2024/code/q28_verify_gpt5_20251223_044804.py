inputs = {'ab2': 41}

def solve(ab2):
    from fractions import Fraction
    from math import gcd

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

    # Given opposite edge squares: A=AB^2=CD^2, B=AC^2=BD^2, C=AD^2=BC^2
    A = ab2
    B = 80
    C = 89

    # In the isosceles disphenoid model with vertices
    # (±x, ±y, ±z) pattern, we get:
    # A = 4(x^2 + y^2), B = 4(x^2 + z^2), C = 4(y^2 + z^2)
    # Solve for x^2, y^2, z^2:
    X = Fraction(B + C - A, 8)  # x^2 (up to permutation)
    Y = Fraction(C + A - B, 8)  # y^2
    Z = Fraction(A + B - C, 8)  # z^2

    # Inradius squared for a disphenoid with parameters x^2=X, y^2=Y, z^2=Z:
    # r^2 = (X Y Z) / (X Y + X Z + Y Z)
    num = X * Y * Z
    den = X * Y + X * Z + Y * Z
    if num == 0:
        return 0

    R2 = num / den
    a = R2.numerator
    b = R2.denominator

    # Reduce a/b first
    g = gcd(a, b)
    a //= g
    b //= g

    # Decompose into square part and squarefree part
    sqa, a_rest = square_part_and_rest(a)
    sqb, b_rest = square_part_and_rest(b)

    # r = sqrt(a/b) = (sqa/sqb) * sqrt(a_rest/b_rest)
    #   = (sqa * sqrt(a_rest*b_rest)) / (sqb * b_rest)
    n_val = a_rest * b_rest
    m0 = sqa
    p0 = sqb * b_rest

    # Ensure n is squarefree (it is if a and b were reduced, but be safe)
    sqn, n_sf = square_part_and_rest(n_val)
    m0 *= sqn

    # Reduce rational factor
    g2 = gcd(m0, p0)
    m = m0 // g2
    p = p0 // g2

    return m + n_sf + p

solve(41)

# 调用 solve
result = solve(inputs['ab2'])
print(result)