inputs = {'ab_sq': 41}

def solve(ab_sq):
    from math import gcd

    def decompose_square(n):
        # Returns (s, r) such that n = s^2 * r, with r squarefree
        n = int(n)
        if n == 0:
            return 0, 1
        if n < 0:
            n = -n
        s = 1
        r = 1
        x = n
        cnt = 0
        while x % 2 == 0:
            x //= 2
            cnt += 1
        if cnt:
            s *= 2 ** (cnt // 2)
            if cnt % 2:
                r *= 2
        p = 3
        while p * p <= x:
            cnt = 0
            while x % p == 0:
                x //= p
                cnt += 1
            if cnt:
                s *= p ** (cnt // 2)
                if cnt % 2:
                    r *= p
            p += 2
        if x > 1:
            r *= x
        return s, r

    a = int(ab_sq)  # AB^2 = CD^2
    b = 80          # AC^2 = BD^2
    c = 89          # AD^2 = BC^2

    # X = a + b - c, Y = a + c - b, Z = b + c - a
    X = a + b - c
    Y = a + c - b
    Z = b + c - a

    # Denominator base = 16 * (area of a face)^2 = 2*(ab+bc+ca) - (a^2+b^2+c^2)
    S1 = a * b + b * c + c * a
    S2 = a * a + b * b + c * c
    denom_base = 2 * S1 - S2

    # r^2 = (X*Y*Z) / (8 * denom_base)
    N = X * Y * Z
    D = 8 * denom_base

    # Reduce fraction
    g = gcd(N, D)
    N //= g
    D //= g

    # Write sqrt(N/D) in the form m*sqrt(n)/p
    sN, rN = decompose_square(N)
    sD, rD = decompose_square(D)

    # sqrt(N/D) = (sN/sD) * sqrt(rN/rD) = (sN*sqrt(rN*rD)) / (sD*rD)
    rad = rN * rD
    sRad, n = decompose_square(rad)
    m = sN * sRad
    p = sD * rD

    g2 = gcd(m, p)
    m //= g2
    p //= g2

    return m + n + p

solve(41)

# 调用 solve
result = solve(inputs['ab_sq'])
print(result)