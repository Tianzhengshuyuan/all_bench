inputs = {'ab2': 41}

def solve(ab2):
    from math import gcd, isqrt

    def factorize(n):
        factors = {}
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors[d] = factors.get(d, 0) + 1
                n //= d
            d = 3 if d == 2 else d + 2
        if n > 1:
            factors[n] = factors.get(n, 0) + 1
        return factors

    def square_decompose(n):
        # return (root_square, free), with n = (root_square**2) * free and free squarefree
        if n == 0:
            return 0, 1
        f = factorize(n)
        root_square = 1
        free = 1
        for p, e in f.items():
            root_square *= p ** (e // 2)
            if e % 2 == 1:
                free *= p
        return root_square, free

    ab2 = int(ab2)
    N = (ab2 + 9) * (ab2 - 9) * (169 - ab2)
    D = 8 * (-ab2 * ab2 + 338 * ab2 - 81)

    if N <= 0 or D <= 0:
        return None

    g = gcd(N, D)
    N //= g
    D //= g

    rootD, d_free = square_decompose(D)
    p0 = rootD * d_free

    K = N * d_free
    rootK, k_free = square_decompose(K)

    m0 = rootK
    n = k_free
    p0 = p0

    g2 = gcd(m0, p0)
    m = m0 // g2
    p = p0 // g2

    return m + n + p

ab2 = 41
solve(ab2)

# 调用 solve
result = solve(inputs['ab2'])
print(result)