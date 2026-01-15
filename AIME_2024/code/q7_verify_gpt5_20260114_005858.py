inputs = {'gon_size': 8}

def solve(gon_size):
    from math import gcd
    n = int(gon_size)
    if n <= 0:
        # Degenerate: 1/1 probability -> m+n = 2
        return 2
    mask = (1 << n) - 1
    total = 1 << n
    good = 0
    for M in range(total):
        ok = False
        for r in range(n):
            if r == 0:
                rotated = M
            else:
                rotated = ((M << r) | (M >> (n - r))) & mask
            if (M & rotated) == 0:
                ok = True
                break
        if ok:
            good += 1
    g = gcd(good, total)
    return good // g + total // g

solve(8)

# 调用 solve
result = solve(inputs['gon_size'])
print(result)