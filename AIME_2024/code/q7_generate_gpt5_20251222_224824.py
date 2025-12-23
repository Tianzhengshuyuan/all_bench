inputs = {'sides': 6}

def solve(sides):
    n = int(sides)
    if n < 0:
        return 0
    allmask = (1 << n) - 1 if n > 0 else 0
    valid = 0
    for mask in range(1 << n):
        found = False
        for t in range(n):
            if n == 0:
                rotated = mask
            else:
                rotated = ((mask << t) | (mask >> (n - t))) & allmask
            if (mask & rotated) == 0:
                found = True
                break
        if found:
            valid += 1
    from math import gcd
    denom = 1 << n
    g = gcd(valid, denom)
    m = valid // g
    d = denom // g
    return m + d

solve(8)

# 调用 solve
result = solve(inputs['sides'])
print(result)