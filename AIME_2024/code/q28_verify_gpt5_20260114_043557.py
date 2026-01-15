inputs = {'ab_sq': 41}

def solve(ab_sq):
    from math import gcd

    # Opposite edge squares
    L1 = int(ab_sq)  # AB^2 = CD^2
    L2 = 80          # AC^2 = BD^2
    L3 = 89          # AD^2 = BC^2

    # r^2 formula for a disphenoid (isosceles tetrahedron)
    X = L1 + L3 - L2
    Y = L1 + L2 - L3
    Z = L2 + L3 - L1

    S1 = L1 * L2 + L2 * L3 + L3 * L1
    S2 = L1 * L1 + L2 * L2 + L3 * L3
    denom_base = 2 * S1 - S2

    N = X * Y * Z
    D = 8 * denom_base

    if D < 0:
        N, D = -N, -D

    g = gcd(abs(N), D)
    N //= g
    D //= g

    if N < 0 or D <= 0:
        # invalid configuration; but for valid input this should not occur
        return 0

    def decompose_square(n):
        # returns s, sf such that n = s^2 * sf and sf is squarefree
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

    sN, fN = decompose_square(N)
    sD, fD = decompose_square(D)

    # r = (sN * sqrt(fN * fD)) / (sD * fD)
    m0 = sN
    p0 = sD * fD
    n = fN * fD

    g2 = gcd(m0, p0)
    m = m0 // g2
    p = p0 // g2

    return m + n + p

solve(41)

# 调用 solve
result = solve(inputs['ab_sq'])
print(result)