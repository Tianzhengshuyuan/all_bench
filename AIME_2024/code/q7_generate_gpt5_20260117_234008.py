inputs = {'n': 11}

def solve(n):
    from math import gcd

    if n <= 0:
        # Degenerate polygon; define probability as 1 (only one coloring, empty),
        # so m/n = 1/1 -> m+n = 2
        return 2

    full = (1 << n) - 1

    def rotate(mask, k):
        k %= n
        if k == 0:
            return mask
        return ((mask << k) | (mask >> (n - k))) & full

    good = 0
    for mask in range(1 << n):
        for k in range(n):
            if (mask & rotate(mask, k)) == 0:
                good += 1
                break

    denom = 1 << n
    g = gcd(good, denom)
    m = good // g
    d = denom // g
    return m + d

solve(8)

# 调用 solve
result = solve(inputs['n'])
print(result)