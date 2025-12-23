inputs = {'n': 3}

def solve(n):
    from math import gcd
    total = 1 << n
    full_mask = total - 1

    def rot(mask, s):
        s %= n
        if s == 0:
            return mask & full_mask
        return ((mask << s) | (mask >> (n - s))) & full_mask

    good = 0
    for mask in range(total):
        ok = False
        for s in range(n):
            if (mask & rot(mask, s)) == 0:
                ok = True
                break
        if ok:
            good += 1

    g = gcd(good, total)
    m = good // g
    den = total // g
    return m + den

solve(8)

# 调用 solve
result = solve(inputs['n'])
print(result)