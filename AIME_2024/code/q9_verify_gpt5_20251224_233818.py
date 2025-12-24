inputs = {'xy': 25}

import math
import cmath

def solve(xy):
    # From equations: N^2 = 4 * xy -> N = 2 * sqrt(xy)
    try:
        if xy >= 0:
            return 2 * math.sqrt(xy)
        else:
            return 2 * cmath.sqrt(xy)
    except TypeError:
        return 2 * cmath.sqrt(xy)

solve(25)

# 调用 solve
result = solve(inputs['xy'])
print(result)