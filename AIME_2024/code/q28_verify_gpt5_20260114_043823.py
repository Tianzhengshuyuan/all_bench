inputs = {'ab_sq': 41}

def solve(ab_sq):
    from math import gcd

    # Opposite edge squares (AB^2=CD^2=L1, AC^2=BD^2=L2, AD^2=BC^2=L3)
    L1 = int(ab_sq)
    L2 = 80
    L3 = 89

    # Define X, Y, Z from edge-square combinations
    X = L1 + L2 - L3
    Y = L1 + L3 - L2
    Z = L2 + L3 - L1

    # Degenerate/invalid configurations guard
    if X <= 0 or Y <= 0 or Z <= 0:
        return 0

    # r^2 = (X * Y * Z) / (8 * (XY + XZ + YZ))
    N = X * Y * Z
    XY = X * Y
    XZ = X * Z
    YZ = Y * Z
    denom_sum = XY + XZ + YZ
    D = 8 * denom_sum

    if N <= 0 or D <= 0:
        return 0

    # Decompose n = s^2 * sf (sf squarefree)
    def decompose_square(n):
        s = 1
        sf = 1
        d = 2
        while d * d <= n:
            cnt = 0
            while n % d == 0:
                n //= d
                cnt += 1
            if cnt:
                s *= d ** (cnt // 2)
                if cnt % 2:
                    sf *= d
            d = 3 if d == 2 else d + 2
        if n > 1:
            sf *= n
        return s, sf

    # Factor numerator and denominator separately
    sN, fN = decompose_square(N)
    sD, fD = decompose_square(D)

    # r = (sN/sD) * sqrt(fN/fD) = (sN * sqrt(fN*fD)) / (sD * fD)
    m0 = sN
    p0 = sD * fD
    n = fN * fD

    # Reduce the rational factor m0/p0
    g = gcd(m0, p0)
    m = m0 // g
    p = p0 // g

    return m + n + p

solve(41)

# 调用 solve
result = solve(inputs['ab_sq'])
print(result)