inputs = {'sides': 8}

def solve(sides):
    n = sides
    total = 1 << n
    allmask = total - 1

    def rotate_left(mask, t):
        t %= n
        if t == 0:
            return mask
        return ((mask << t) & allmask) | (mask >> (n - t))

    favorable = 0
    for mask in range(total):
        if mask == 0:
            favorable += 1
            continue
        ok = False
        rot = rotate_left(mask, 1)
        for _ in range(1, n):
            if (rot & mask) == 0:
                ok = True
                break
            rot = rotate_left(rot, 1)
        if ok:
            favorable += 1

    from math import gcd
    g = gcd(favorable, total)
    m = favorable // g
    den = total // g
    return m + den

solve(sides)

# 调用 solve
result = solve(inputs['sides'])
print(result)