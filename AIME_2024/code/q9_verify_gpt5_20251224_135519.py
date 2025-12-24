inputs = {'xy': 25}

import math

def solve(xy):
    if xy < 0:
        return None
    return 2 * math.sqrt(xy)

solve(25)

# 调用 solve
result = solve(inputs['xy'])
print(result)