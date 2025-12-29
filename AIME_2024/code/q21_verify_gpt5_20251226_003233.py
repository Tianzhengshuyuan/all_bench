inputs = {'b': 211}

def solve(b):
    import math

    def count_beautiful(base):
        if base < 2:
            return 0
        # Count pairs (x,y) with x in [1,b-1], y in [0,b-1], such that
        # n = bx + y is a perfect square and sqrt(n) = x + y (= z).
        # This is equivalent to z(z-1) = (base-1)*x with z = x + y and
        # z^2 = n in [base, base^2-1], so z in [ceil(sqrt(base)), base-1].
        z_min = math.isqrt(base)
        if z_min * z_min < base:
            z_min += 1
        cnt = 0
        for z in range(max(2, z_min), base):
            zz1 = z * (z - 1)
            if zz1 % (base - 1) != 0:
                continue
            x = zz1 // (base - 1)
            if 1 <= x <= base - 1:
                y = z - x
                if 0 <= y <= base - 1:
                    cnt += 1
        return cnt

    c_b = count_beautiful(b)
    # Max count for bases < b
    M = 0
    for t in range(2, b):
        M = max(M, count_beautiful(t))

    # Return the largest N such that b is the least base with more than N b-eautiful integers
    # This corresponds to the maximal count attained by any base < b.
    if c_b <= M:
        return -1
    return M

solve(211)

# 调用 solve
result = solve(inputs['b'])
print(result)