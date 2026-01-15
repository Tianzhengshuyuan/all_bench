inputs = {'ab_sq': 41}

def solve(ab_sq):
    from math import gcd

    L1 = int(ab_sq)
    L2 = 80
    L3 = 89

    S1 = L1 * L2 + L2 * L3 + L3 * L1
    S2 = L1 * L1 + L2 * L2 + L3 * L3
    denom_base = 2 * S1 - S2  # equals 16 * area^2 of a face

    Xn = L1 + L3 - L2
    Yn = L1 + L2 - L3
    Zn = L2 + L3 - L1

    N = Xn * Yn * Zn
    D = 8 * denom_base  # r^2 = N / D

    if D < 0:
        N, D = -N, -D
    g = gcd(abs(N), D)
    N //= g
    D //= g

    P = N * D  # r = sqrt(P) / D
    if P < 0:
        P = -P  # ensure non-negative under sqrt for valid configurations

    def square_part(n):
        k = 1
        sf = 1
        d = 2
        while d * d <= n:
            cnt = 0
            while n % d == 0:
                n //= d
                cnt += 1
            if cnt:
                if cnt // 2:
                    k *= d ** (cnt // 2)
                if cnt % 2 == 1:
                    sf *= d
            d = 3 if d == 2 else d + 2
        if n > 1:
            sf *= n
        return k, sf

    k, n_sf = square_part(P)

    g2 = gcd(k, D)
    m = k // g2
    p = D // g2
    n = n_sf

    return m + n + p

solve(41)

# 调用 solve
result = solve(inputs['ab_sq'])
print(result)