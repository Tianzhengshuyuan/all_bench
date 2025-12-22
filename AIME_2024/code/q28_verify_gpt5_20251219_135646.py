inputs = {'ac_bd_sq': 80}

def solve(ac_bd_sq):
    from fractions import Fraction
    from math import gcd

    def squarefree_decompose(n):
        n = abs(n)
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

    # Solve for x^2, y^2, z^2 via the disphenoid box model
    X = Fraction(ab_cd_sq + ad_bc_sq - ac_bd_sq, 2)
    Y = Fraction(ab_cd_sq + ac_bd_sq - ad_bc_sq, 2)
    Z = Fraction(ac_bd_sq + ad_bc_sq - ab_cd_sq, 2)

    # r = (1/2) * sqrt( (XYZ) / (XY + YZ + ZX) )
    N_num = X * Y * Z
    N_den = X * Y + Y * Z + Z * X

    R = N_num / N_den  # Reduced fraction
    N = R.numerator
    D = R.denominator

    # sqrt(N/D) = sqrt(N*D) / D
    K = N * D
    sq_factor, rad = squarefree_decompose(K)

    m0 = sq_factor
    p0 = 2 * D
    g2 = gcd(m0, p0)
    m = m0 // g2
    p = p0 // g2
    n = rad

    return m + n + p

solve(80)

# 调用 solve
result = solve(inputs['ac_bd_sq'])
print(result)