inputs = {'ac_bd_sq': 80}

def solve(ac_bd_sq):
    from math import gcd

    def squarefree_decompose(n):
        sq = 1
        sf = 1
        d = 2
        while d * d <= n:
            cnt = 0
            while n % d == 0:
                n //= d
                cnt += 1
            if cnt:
                sq *= d ** (cnt // 2)
                if cnt % 2 == 1:
                    sf *= d
            d += 1 if d == 2 else 2
        if n > 1:
            sf *= n
        return sq, sf

    ab_cd_sq = 41
    ad_bc_sq = 89

    # Let X = x^2, Y = y^2, Z = z^2 for the box model of a disphenoid
    X = (ab_cd_sq + ad_bc_sq - ac_bd_sq) // 2
    Y = (ab_cd_sq + ac_bd_sq - ad_bc_sq) // 2
    Z = (ac_bd_sq + ad_bc_sq - ab_cd_sq) // 2

    # r = (1/2) * sqrt( (XYZ) / (XY + YZ + ZX) )
    N_num = X * Y * Z
    N_den = X * Y + Y * Z + Z * X

    g = gcd(N_num, N_den)
    num1 = N_num // g
    den1 = N_den // g

    # sqrt(num1/den1) = sqrt(num1*den1) / den1
    K = num1 * den1
    sq_factor, rad = squarefree_decompose(K)

    m0 = sq_factor
    p0 = 2 * den1
    g2 = gcd(m0, p0)
    m = m0 // g2
    p = p0 // g2
    n = rad

    return m + n + p

solve(80)

# 调用 solve
result = solve(inputs['ac_bd_sq'])
print(result)