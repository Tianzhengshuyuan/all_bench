inputs = {'m+n': 371}

def solve(m_plus_n):
    import math

    def rotate_left8(x, r):
        return ((x << r) | (x >> (8 - r))) & 0xFF

    favorable = 0
    total = 1 << 8  # 2^8 colorings

    for b in range(total):  # b is bitmask of blue vertices
        ok = False
        for r in range(8):  # all rotations
            if (rotate_left8(b, r) & b) == 0:
                ok = True
                break
        if ok:
            favorable += 1

    g = math.gcd(favorable, total)
    m, n = favorable // g, total // g
    return f"{m}/{n}"

solve(371)

# 调用 solve
result = solve(inputs['m+n'])
print(result)