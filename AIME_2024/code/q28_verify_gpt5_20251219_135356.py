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

    # x = S - ac_bd_sq, y = S - ad_bc_sq, z = S - ab_cd_sq without explicitly computing S
    x = (ab_cd_sq + ad_bc_sq - ac_bd_sq) // 2
    y = (ab_cd_sq + ac_bd_sq - ad_bc_sq) // 2
    z = (ac_bd_sq + ad_bc_sq - ab_cd_sq) // 2

    N_num = x * y * z
    N_den = x * y + y * z + z * x

    g = gcd(N_num, N_den)
    num1 = N_num // g
    den1 = N_den // g

    # r = sqrt(num1/den1)/2 = sqrt(num1*den1)/(2*den1)
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