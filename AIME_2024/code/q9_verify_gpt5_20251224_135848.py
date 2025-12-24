inputs = {'xy': 25}

import math

def solve(xy):
    N = 2 * math.sqrt(xy)
    r = round(N)
    if abs(N - r) < 1e-12:
        return int(r)
    return N

solve(25)

# 调用 solve
result = solve(inputs['xy'])
print(result)