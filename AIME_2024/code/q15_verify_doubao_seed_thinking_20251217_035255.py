inputs = {'grid_size': 8}

import math

def solve(grid_size):
    return 2 * math.comb(grid_size - 1, 2) * math.comb(grid_size - 1, 1)

# 调用 solve
result = solve(inputs['grid_size'])
print(result)