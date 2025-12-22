inputs = {'sqrt_arg_AC_BD': 80}

def solve(sqrt_arg_AC_BD: int) -> int:
    import math

    AB2 = 41
    AC2 = sqrt_arg_AC_BD
    AD2 = 89

    S2 = AB2 + AC2 + AD2
    if S2 % 2 != 0:
        raise ValueError("Invalid input leading to non-integer parameters.")
    S = S2 // 2

    # u^2 = X, v^2 = Y, w^2 = Z
    X = S - AB2
    Y = S - AD2
    Z = S - AC2
    if X <= 0 or Y <= 0 or Z <= 0:
        raise ValueError("Invalid input leading to non-positive squared parameters.")

    # M = u^2 (v^2 + w^2) + v^2 w^2
    M = X * (Y + Z) + Y * Z
    # A = X Y Z
    A = X * Y * Z
    Q = A * M  # r = sqrt(Q) / (2M)

    def squarefree_sqrt_parts(n: int):
        # returns (t, n_sf) with n = t^2 * n_sf, and n_sf squarefree
        t = 1
        n_sf = 1
        d = 2
        while d * d <= n:
            cnt = 0
            while n % d == 0:
                n //= d
                cnt += 1
            if cnt:
                t *= d ** (cnt // 2)
                if cnt % 2 == 1:
                    n_sf *= d
            d += 1 if d == 2 else 2  # after 2, test only odd
        if n > 1:
            # n is prime now
            n_sf *= n
        return t, n_sf

    t, n_sf = squarefree_sqrt_parts(Q)
    numerator = t
    denominator = 2 * M

    g = math.gcd(numerator, denominator)
    m = numerator // g
    p = denominator // g
    n = n_sf

    return m + n + p

# 调用 solve
result = solve(inputs['sqrt_arg_AC_BD'])
print(result)