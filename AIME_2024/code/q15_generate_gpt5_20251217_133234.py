inputs = {'size': 117}

import math

def solve(size):
    if size < 2:
        return 0
    return 2 * math.comb(size - 1, 2) * math.comb(size - 1, 1)

# 调用 solve
result = solve(inputs['size'])
print(result)