inputs = {'b': 211}

def solve(b):
    import math

    def count_beautiful(base):
        if base < 2:
            return 0
        b1 = base - 1
        # z must satisfy: z^2 = base*x + y, with x+y = z, x in [1, b-1], y in [0, b-1]
        # Equivalent: z(z-1) = (base-1)*x and n=z^2 must be a two-digit base-base number => z^2 >= base
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

    # If b is not a new record, no such N exists; return -1 to indicate impossibility
    if c_b <= M:
        return -1
    # Largest N such that b is the least base with more than N b-eautiful integers
    return c_b - 1

solve(211)

# 调用 solve
result = solve(inputs['b'])
print(result)