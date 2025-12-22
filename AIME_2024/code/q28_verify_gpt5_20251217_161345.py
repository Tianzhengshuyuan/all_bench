inputs = {'sqrt_arg_AC_BD': 80}

def solve(sqrt_arg_AC_BD: int) -> int:
    import math

    # Edge lengths squared
    AB2 = 41
    AC2 = sqrt_arg_AC_BD
    AD2 = 89
    BC2 = 89
    BD2 = sqrt_arg_AC_BD
    CD2 = 41

    # Cayley-Menger determinant via Bareiss algorithm (exact integer arithmetic)
    def det_bareiss(mat):
        n = len(mat)
        A = [row[:] for row in mat]
        sign = 1
        denom = 1
        for k in range(n - 1):
            # Pivoting if needed
            if A[k][k] == 0:
                pivot_row = None
                for i in range(k + 1, n):
                    if A[i][k] != 0:
                        pivot_row = i
                        break
                if pivot_row is None:
                    return 0
                A[k], A[pivot_row] = A[pivot_row], A[k]
                sign = -sign
            pivot = A[k][k]
            for i in range(k + 1, n):
                for j in range(k + 1, n):
                    A[i][j] = (A[i][j] * pivot - A[i][k] * A[k][j]) // denom
                A[i][k] = 0
            denom = pivot
        return sign * A[n - 1][n - 1]

    # Build Cayley-Menger matrix
    CM = [
        [0,   1,    1,    1,    1],
        [1,   0,  AB2,  AC2,  AD2],
        [1, AB2,    0,  BC2,  BD2],
        [1, AC2,  BC2,    0,  CD2],
        [1, AD2,  BD2,  CD2,    0],
    ]
    Delta = det_bareiss(CM)
    if Delta < 0:
        Delta = -Delta  # Should be nonnegative for a valid tetrahedron

    # Total surface area S_total:
    # For disphenoid, all faces are congruent with sides sqrt(41), sqrt(AC2), sqrt(89).
    # Using 16A^2 = 2(sum a^2 b^2) - (a^4 + b^4 + c^4)
    x, y, z = AB2, AC2, AD2  # squares of side lengths for any face (AB, AC, AD) -> same multiset as any face
    NA = 2 * (x * y + y * z + z * x) - (x * x + y * y + z * z)  # equals (4A)^2, so S_total = sqrt(NA)

    # Inradius r satisfies: r = 3V / S_total, and V^2 = Delta / 288
    # Hence r^2 = Delta / (32 * NA)
    num = Delta
    den = 32 * NA

    # Reduce fraction first
    g = math.gcd(num, den)
    num //= g
    den //= g

    # Decompose into squarefree parts: n = t^2 * s (s squarefree)
    def squarefree_decompose(n: int):
        t = 1
        s = 1
        d = 2
        m = n
        while d * d <= m:
            cnt = 0
            while m % d == 0:
                m //= d
                cnt += 1
            if cnt:
                t *= d ** (cnt // 2)
                if cnt % 2 == 1:
                    s *= d
            d += 1 if d == 2 else 2
        if m > 1:
            # remaining prime
            s *= m
        return t, s

    a, s1 = squarefree_decompose(num)
    b, s2 = squarefree_decompose(den)

    # r = (a/b) * sqrt(s1/s2) = (a/b) * sqrt(s1*s2) / s2
    w = s1 * s2
    c, u = squarefree_decompose(w)

    m_num = a * c
    p_den = b * s2
    # reduce final fraction
    g2 = math.gcd(m_num, p_den)
    m = m_num // g2
    p = p_den // g2
    n = u

    return m + n + p

# 调用 solve
result = solve(inputs['sqrt_arg_AC_BD'])
print(result)