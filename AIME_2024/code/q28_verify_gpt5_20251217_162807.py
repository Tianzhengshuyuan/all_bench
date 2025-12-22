inputs = {'sqrt_arg_AC_BD': 80}

from fractions import Fraction
from math import gcd, isqrt

def solve(sqrt_arg_AC_BD: int) -> int:
    # Given: AB^2 = 41, AC^2 = sqrt_arg_AC_BD, AD^2 = 89
    a = 41
    b = sqrt_arg_AC_BD
    c = 89

    # Solve for x^2, y^2, z^2 in the disphenoid model:
    # x^2 + y^2 = a, x^2 + z^2 = b, y^2 + z^2 = c
    x2 = Fraction(a + b - c, 2)
    y2 = Fraction(a + c - b, 2)
    z2 = Fraction(b + c - a, 2)

    # r^2 = (x^2 y^2 z^2) / (4 (x^2 y^2 + x^2 z^2 + y^2 z^2))
    X = x2 * y2 * z2
    Y = x2 * y2 + x2 * z2 + y2 * z2
    r2 = X / (4 * Y)
    P, Q = r2.numerator, r2.denominator  # r^2 = P/Q

    # r = sqrt(P/Q) = sqrt(P*Q)/Q; write as m*sqrt(n)/p with n squarefree
    T = P * Q

    # Extract largest square factor from T
    def squarefree_decompose(n: int):
        k = 1  # product of square roots of square factors
        sf = 1  # squarefree part
        t = n
        i = 2
        while i * i <= t:
            cnt = 0
            while t % i == 0:
                t //= i
                cnt += 1
            if cnt:
                k *= i ** (cnt // 2)
                if cnt % 2 == 1:
                    sf *= i
            i += 1 if i == 2 else 2  # small optimization: after 2, check only odd
        if t > 1:
            # remaining prime with exponent 1
            sf *= t
        return k, sf

    k, n_sf = squarefree_decompose(T)

    # r = k*sqrt(n_sf) / Q, reduce m and p by gcd
    g = gcd(k, Q)
    m = k // g
    p = Q // g
    n = n_sf

    return m + n + p

# 调用 solve
result = solve(inputs['sqrt_arg_AC_BD'])
print(result)