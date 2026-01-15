inputs = {'ac_bd_sq': 114}

def solve(ac_bd_sq):
    from fractions import Fraction
    from math import isqrt, gcd

    def squarefree_decomp(n):
        # returns (d, sf) such that n = d^2 * sf and sf is squarefree
        n = int(n)
        d = 1
        sf = 1
        if n <= 1:
            return (1, n)
        # factor 2
        e = 0
        while n % 2 == 0:
            n //= 2
            e += 1
        if e:
            d *= 2 ** (e // 2)
            if e % 2:
                sf *= 2
        p = 3
        while p * p <= n:
            e = 0
            while n % p == 0:
                n //= p
                e += 1
            if e:
                d *= p ** (e // 2)
                if e % 2:
                    sf *= p
            p += 2
        if n > 1:
            sf *= n
        return (d, sf)

    # Given: AB^2 = 41, BC^2 = 89, AC^2 = ac_bd_sq (parameter)
    ab_sq = Fraction(41)
    bc_sq = Fraction(89)
    ac_sq = Fraction(ac_bd_sq)

    x2 = (ab_sq + ac_sq - bc_sq) / 2
    y2 = (ab_sq + bc_sq - ac_sq) / 2
    z2 = (ac_sq + bc_sq - ab_sq) / 2

    inv_sum = Fraction(1, 1) / x2 + Fraction(1, 1) / y2 + Fraction(1, 1) / z2
    a = inv_sum.numerator
    b = inv_sum.denominator

    da, a_sf = squarefree_decomp(a)
    N = b * a_sf
    dN, n_sf = squarefree_decomp(N)

    m0 = dN
    p0 = 2 * da * a_sf
    g = gcd(m0, p0)
    m = m0 // g
    p = p0 // g
    n = n_sf

    return m + n + p

ac_bd_sq = 80
solve(ac_bd_sq)

# 调用 solve
result = solve(inputs['ac_bd_sq'])
print(result)