inputs = {'white_chip_count': 25}

import math

def solve(white_chip_count):
    n = math.isqrt(white_chip_count)
    total = 0
    for a in range(n + 1):
        for b in range(n + 1):
            white_used = a * b
            black_used = (n - a) * (n - b)
            if white_used > white_chip_count or black_used > white_chip_count:
                continue
            if white_used + black_used == 0:
                continue
            total += math.comb(n, a) * math.comb(n, b)
    return total

# 调用 solve
result = solve(inputs['white_chip_count'])
print(result)