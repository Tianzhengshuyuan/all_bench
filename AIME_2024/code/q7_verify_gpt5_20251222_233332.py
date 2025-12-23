inputs = {'sides': 8}

def solve(sides):
    from math import gcd
    n = sides
    total = 1 << n
    mask_all = total - 1

    def rot(mask, s):
        s %= n
        if s == 0:
            return mask & mask_all
        res = 0
        for i in range(n):
            j = (i - s) % n
            if (mask >> j) & 1:
                res |= (1 << i)
        return res

    good = 0
    for mask in range(total):
        for s in range(n):
            if (mask & rot(mask, s)) == 0:
                good += 1
                break

    g = gcd(good, total)
    m = good // g
    d = total // g
    return m + d

solve(8)

# 调用 solve
result = solve(inputs['sides'])
print(result)