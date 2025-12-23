inputs = {'sides': 8}

def solve(sides):
    from math import gcd
    n = sides
    total = 1 << n
    mask_all = total - 1

    def rot(mask, k):
        k %= n
        if k == 0:
            return mask & mask_all
        return ((mask << k) | (mask >> (n - k))) & mask_all

    favorable = 0
    for m in range(total):
        ok = False
        for k in range(n):
            if (m & rot(m, k)) == 0:
                ok = True
                break
        if ok:
            favorable += 1

    g = gcd(favorable, total)
    m_red = favorable // g
    n_red = total // g
    return m_red + n_red

solve(8)

# 调用 solve
result = solve(inputs['sides'])
print(result)