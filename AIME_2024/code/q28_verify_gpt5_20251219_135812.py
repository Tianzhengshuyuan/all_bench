inputs = {'ac_bd_sq': 80}

def solve(ac_bd_sq):
    from math import gcd

    # extract largest square factor: n = sq^2 * rem, rem squarefree
    def square_factor(n):
        f = 1
        rem = n
        d = 2
        while d * d <= rem:
            cnt = 0
            while rem % d == 0:
                rem //= d
                cnt += 1
            if cnt:
                f *= d ** (cnt // 2)
            d += 1
        return f, rem

    # Given: AB^2=CD^2=41, AC^2=BD^2=ac_bd_sq, AD^2=BC^2=89
    s_ab_cd = 41
    s_ac_bd = ac_bd_sq
    s_ad_bc = 89

    # Solve for x^2=u, y^2=v, z^2=w
    u = (s_ab_cd + s_ad_bc - s_ac_bd) // 2
    v = (s_ab_cd + s_ac_bd - s_ad_bc) // 2
    w = (s_ac_bd + s_ad_bc - s_ab_cd) // 2

    # r = (1/2) * sqrt( (u v w) / (u v + v w + w u) )
    U = u * v * w
    D = u * v + v * w + w * u

    g = gcd(U, D)
    num = U // g
    den = D // g

    sqnum, remnum = square_factor(num)
    sqden, remden = square_factor(den)

    X = remnum * remden
    t, n_sqfree = square_factor(X)

    m_num = sqnum * t
    p_den = 2 * sqden * remden

    g2 = gcd(m_num, p_den)
    m = m_num // g2
    p = p_den // g2
    n = n_sqfree

    return m + n + p

solve(80)

# 调用 solve
result = solve(inputs['ac_bd_sq'])
print(result)