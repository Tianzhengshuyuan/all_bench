inputs = {'sides': 11}

from math import gcd

def solve(sides):
    n = sides
    if n <= 0:
        return 2
    mask = (1 << n) - 1
    good = 0
    for x in range(1 << n):
        for k in range(n):
            xk = ((x << k) | (x >> (n - k))) & mask
            if (x & xk) == 0:
                good += 1
                break
    denom = 1 << n
    g = gcd(good, denom)
    m = good // g
    dn = denom // g
    return m + dn

solve(8)

# 调用 solve
result = solve(inputs['sides'])
print(result)