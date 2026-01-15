inputs = {'ab_sq': 41}

def solve(ab_sq):
    from math import gcd

    def square_decompose(n):
        if n == 0:
            return 0, 1
        sq = 1
        original = n
        d = 2
        nn = n
        while d * d <= nn:
            cnt = 0
            while nn % d == 0:
                nn //= d
                cnt += 1
            if cnt:
                sq *= d ** (cnt // 2)
            d += 1 if d == 2 else 2
        rem = original // (sq * sq)
        return sq, rem

    A = ab_sq
    # r^2 = ((A^2 - 81)*(169 - A)) / (8*(-A^2 + 338A - 81))
    num = (A * A - 81) * (169 - A)
    den = 8 * (-A * A + 338 * A - 81)
    if den < 0:
        num = -num
        den = -den
    g = gcd(abs(num), den)
    num //= g
    den //= g
    if num == 0:
        m, n, p = 0, 1, 1
        return m + n + p
    snum, n0 = square_decompose(abs(num))
    sden, d0 = square_decompose(den)
    m = snum
    n = n0 * d0
    p = sden * d0
    g2 = gcd(m, p)
    m //= g2
    p //= g2
    return m + n + p

solve(ab_sq)

# 调用 solve
result = solve(inputs['ab_sq'])
print(result)