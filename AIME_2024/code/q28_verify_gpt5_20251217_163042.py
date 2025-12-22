inputs = {'sqrt_arg_AC_BD': 80}

def solve(sqrt_arg_AC_BD: int) -> int:
    import math

    # Given squared lengths of opposite edges (isosceles disphenoid)
    u = 41  # AB^2 = CD^2
    v = sqrt_arg_AC_BD  # AC^2 = BD^2
    w = 89  # AD^2 = BC^2

    # Solve for a^2, b^2, c^2 from:
    # a^2 + b^2 = u, b^2 + c^2 = v, c^2 + a^2 = w
    s1 = u + w - v
    s2 = u + v - w
    s3 = v + w - u
    if (s1 | s2 | s3) & 1:
        raise ValueError("Invalid input leading to non-integer a^2, b^2, c^2.")
    a2 = s1 // 2
    b2 = s2 // 2
    c2 = s3 // 2
    if a2 <= 0 or b2 <= 0 or c2 <= 0:
        raise ValueError("Invalid input leading to non-positive a^2, b^2, c^2.")

    # Inradius squared for isosceles disphenoid:
    # r^2 = (a^2 b^2 c^2) / (4*(a^2 b^2 + b^2 c^2 + c^2 a^2))
    num = a2 * b2 * c2
    den = 4 * (a2 * b2 + b2 * c2 + c2 * a2)

    # Reduce fraction first
    g = math.gcd(num, den)
    num //= g
    den //= g

    # Decompose n into k^2 * s (s squarefree), return (k, s)
    def squarefree_decompose(n: int):
        k = 1
        s = 1
        d = 2
        m = n
        while d * d <= m:
            cnt = 0
            while m % d == 0:
                m //= d
                cnt += 1
            if cnt:
                k *= d ** (cnt // 2)
                if cnt % 2 == 1:
                    s *= d
            d += 1 if d == 2 else 2  # after 2, test only odd
        if m > 1:
            s *= m
        return k, s

    # Write r = sqrt(num/den) = (a/b) * sqrt(s1/s2) = (a * sqrt(s1*s2)) / (b * s2)
    a, s1_sf = squarefree_decompose(num)
    b, s2_sf = squarefree_decompose(den)
    c, n = squarefree_decompose(s1_sf * s2_sf)

    m_num = a * c
    p_den = b * s2_sf

    g2 = math.gcd(m_num, p_den)
    m = m_num // g2
    p = p_den // g2

    return m + n + p

# 调用 solve
result = solve(inputs['sqrt_arg_AC_BD'])
print(result)