inputs = {'sqrt_arg_AC_BD': 80}

def solve(sqrt_arg_AC_BD: int) -> int:
    import math

    # Opposite edges equal (isosceles disphenoid)
    u = 41  # AB^2 = CD^2
    v = sqrt_arg_AC_BD  # AC^2 = BD^2
    w = 89  # AD^2 = BC^2

    # Solve for a^2, b^2, c^2 from:
    # a^2 + b^2 = u, b^2 + c^2 = v, c^2 + a^2 = w
    s1 = u + w - v
    s2 = u + v - w
    s3 = v + w - u
    if s1 % 2 != 0 or s2 % 2 != 0 or s3 % 2 != 0:
        raise ValueError("Invalid input: a^2, b^2, c^2 are not integers.")
    a2 = s1 // 2
    b2 = s2 // 2
    c2 = s3 // 2
    if a2 <= 0 or b2 <= 0 or c2 <= 0:
        raise ValueError("Invalid input: non-positive a^2, b^2, or c^2.")

    # Inradius squared for isosceles disphenoid:
    # r^2 = (a^2 b^2 c^2) / (4*(a^2 b^2 + b^2 c^2 + c^2 a^2))
    num = a2 * b2 * c2
    den = 4 * (a2 * b2 + b2 * c2 + c2 * a2)

    # Reduce fraction
    g = math.gcd(num, den)
    num //= g
    den //= g

    # Decompose integer n into k^2 * s (s squarefree)
    def squarefree_decompose(n: int):
        k = 1
        s = 1
        t = n
        d = 2
        while d * d <= t:
            cnt = 0
            while t % d == 0:
                t //= d
                cnt += 1
            if cnt:
                k *= d ** (cnt // 2)
                if cnt % 2 == 1:
                    s *= d
            d += 1 if d == 2 else 2  # after 2, check only odd numbers
        if t > 1:
            s *= t
        return k, s

    # r = sqrt(num/den) = sqrt(num*den)/den = (k * sqrt(sf)) / den
    T = num * den
    k, n_sf = squarefree_decompose(T)

    g2 = math.gcd(k, den)
    m = k // g2
    p = den // g2
    n = n_sf

    return m + n + p

# 调用 solve
result = solve(inputs['sqrt_arg_AC_BD'])
print(result)