inputs = {'probability_denominator': 256}

import math

def solve(probability_denominator):
    n = 8
    mask = (1 << n) - 1
    count = 0
    for S in range(1 << n):
        ok = False
        for k in range(1, n):
            rot = ((S << k) | (S >> (n - k))) & mask
            if (S & rot) == 0:
                ok = True
                break
        if ok:
            count += 1
    g = math.gcd(count, probability_denominator)
    m = count // g
    d = probability_denominator // g
    return m + d

solve(256)

# 调用 solve
result = solve(inputs['probability_denominator'])
print(result)