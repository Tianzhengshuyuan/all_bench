inputs = {}

def solve(_):
    import math

    # Given squared lengths of adjacent edges from the rectangular prism embedding
    AB2, AC2, BC2 = 41, 80, 89

    # Solve for a^2, b^2, c^2 where:
    # AB^2 = a^2 + b^2, AC^2 = a^2 + c^2, BC^2 = b^2 + c^2
    a2 = (AB2 + AC2 - BC2) // 2
    b2 = (AB2 + BC2 - AC2) // 2
    c2 = (AC2 + BC2 - AB2) // 2

    a = int(math.isqrt(a2))
    b = int(math.isqrt(b2))
    c = int(math.isqrt(c2))

    # r = abc / (2 * sqrt(a^2 b^2 + b^2 c^2 + c^2 a^2))
    N = a * b * c
    S = a2 * b2 + b2 * c2 + c2 * a2

    def squarefree_decomp(n):
        s0, t = 1, 1
        d = 2
        while d * d <= n:
            cnt = 0
            while n % d == 0:
                n //= d
                cnt += 1
            if cnt:
                t *= d ** (cnt // 2)
                if cnt % 2 == 1:
                    s0 *= d
            d += 1
        if n > 1:
            s0 *= n
        return s0, t

    n_sqfree, t_sq = squarefree_decomp(S)
    denom = 2 * t_sq * n_sqfree
    g = math.gcd(N, denom)
    m = N // g
    p = denom // g
    n = n_sqfree

    return m + n + p

solve({})

# 调用 solve
result = solve(inputs)
print(result)