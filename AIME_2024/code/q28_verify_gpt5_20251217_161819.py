inputs = {'sqrt_arg_AC_BD': 80}

def solve(sqrt_arg_AC_BD: int) -> int:
    import math

    # Opposite edges equal (isosceles disphenoid)
    u = 41  # AB^2 = CD^2
    v = sqrt_arg_AC_BD  # AC^2 = BD^2
    w = 89  # AD^2 = BC^2

    # Solve for a^2, b^2, c^2 with:
    # a^2 + b^2 = u, b^2 + c^2 = v, c^2 + a^2 = w
    s1 = u + w - v
    s2 = u + v - w
    s3 = v + w - u
    a2 = s1 // 2
    b2 = s2 // 2
    c2 = s3 // 2

    # Inradius r for isosceles disphenoid (coordinates model):
    # r^2 = (a^2 b^2 c^2) / (4*(a^2 b^2 + b^2 c^2 + c^2 a^2))
    num = a2 * b2 * c2
    den = 4 * (a2 * b2 + b2 * c2 + c2 * a2)

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

    # Write sqrt(num/den) as (m sqrt(n))/p
    a, n1 = squarefree_decompose(num)
    b, n2 = squarefree_decompose(den)
    c, n = squarefree_decompose(n1 * n2)

    m_num = a * c
    p_den = b * n2
    g2 = math.gcd(m_num, p_den)
    m = m_num // g2
    p = p_den // g2

    return m + n + p

# 调用 solve
result = solve(inputs['sqrt_arg_AC_BD'])
print(result)