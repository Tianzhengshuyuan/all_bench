inputs = {'sqrt_arg_AC_BD': 80}

def solve(sqrt_arg_AC_BD: int) -> int:
    import math

    # Squared lengths of opposite edges (isosceles disphenoid)
    u = 41  # AB^2 = CD^2
    v = sqrt_arg_AC_BD  # AC^2 = BD^2
    w = 89  # AD^2 = BC^2

    # Solve for a^2, b^2, c^2 from:
    # a^2 + b^2 = u, b^2 + c^2 = v, c^2 + a^2 = w
    s1 = u + w - v
    s2 = u + v - w
    s3 = v + w - u
    if s1 % 2 or s2 % 2 or s3 % 2:
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

    g = math.gcd(num, den)
    num //= g
    den //= g

    def sqrt_parts(n: int):
        # returns (k, s) such that sqrt(n) = k * sqrt(s), with s squarefree
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
            d += 1 if d == 2 else 2
        if m > 1:
            s *= m
        return k, s

    # Write r = sqrt(num/den) = (u/v) * sqrt(s1/s2)
    u1, s1_sf = sqrt_parts(num)
    v1, s2_sf = sqrt_parts(den)

    # Rationalize: sqrt(s1/s2) = sqrt(s1*s2) / s2
    w1, s_sf = sqrt_parts(s1_sf * s2_sf)

    m_num = u1 * w1
    p_den = v1 * s2_sf

    g2 = math.gcd(m_num, p_den)
    m = m_num // g2
    p = p_den // g2
    n = s_sf

    return m + n + p

# 调用 solve
result = solve(inputs['sqrt_arg_AC_BD'])
print(result)