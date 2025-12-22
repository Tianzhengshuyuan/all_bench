inputs = {'sqrt_arg_AC_BD': 80}

def solve(sqrt_arg_AC_BD: int) -> int:
    import math

    # Given squared edge lengths (pairs of opposite edges equal)
    u = 41  # AB^2 = CD^2
    v = sqrt_arg_AC_BD  # AC^2 = BD^2
    w = 89  # AD^2 = BC^2

    # Recover a^2, b^2, c^2 such that:
    # a^2 + b^2 = u, b^2 + c^2 = v, c^2 + a^2 = w
    a2 = (u + w - v) // 2
    b2 = (u + v - w) // 2
    c2 = (v + w - u) // 2

    # Inradius r for isosceles disphenoid with coordinates
    # A(0,0,0), B(a,b,0), C(0,b,c), D(a,0,c):
    # V = abc/3, each face area = (1/2)*sqrt(a^2 b^2 + b^2 c^2 + c^2 a^2)
    # Total surface area S = 4 * area(face) = 2*sqrt(sum)
    # r = 3V/S = abc / (2*sqrt(sum))
    # So r^2 = (a^2 b^2 c^2) / (4*(a^2 b^2 + b^2 c^2 + c^2 a^2))
    P = a2 * b2 * c2
    Ssum = a2 * b2 + b2 * c2 + c2 * a2

    num = P
    den = 4 * Ssum

    g = math.gcd(num, den)
    num //= g
    den //= g

    def squarefree_decompose(n: int):
        t = 1
        s = 1
        d = 2
        while d * d <= n:
            cnt = 0
            while n % d == 0:
                n //= d
                cnt += 1
            if cnt:
                t *= d ** (cnt // 2)
                if cnt % 2 == 1:
                    s *= d
            d += 1 if d == 2 else 2
        if n > 1:
            s *= n
        return t, s

    # r = sqrt(num/den) = (a/b) * sqrt(n1/n2) = (a*c / (b*n2)) * sqrt(n)
    a, n1 = squarefree_decompose(num)
    b, n2 = squarefree_decompose(den)
    wprod = n1 * n2
    c, n = squarefree_decompose(wprod)

    m_num = a * c
    p_den = b * n2
    g2 = math.gcd(m_num, p_den)
    m = m_num // g2
    p = p_den // g2

    return m + n + p

# 调用 solve
result = solve(inputs['sqrt_arg_AC_BD'])
print(result)