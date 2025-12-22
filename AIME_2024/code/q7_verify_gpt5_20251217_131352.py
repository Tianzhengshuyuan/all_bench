inputs = {'n': 7}

import math

def solve(n):
    sides = 8  # regular octagon
    total = 1 << sides
    fullmask = total - 1

    def rotate(mask, k):
        k %= sides
        if k == 0:
            return mask & fullmask
        return ((mask << k) & fullmask) | (mask >> (sides - k))

    valid = 0
    for mask in range(total):
        ok = False
        for k in range(sides):
            if (rotate(mask, k) & mask) == 0:
                ok = True
                break
        if ok:
            valid += 1

    g = math.gcd(valid, total)
    num = valid // g
    den = total // g
    return num + den

# 调用 solve
result = solve(inputs['n'])
print(result)