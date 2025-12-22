inputs = {'grid_rows': 665}

import math

def solve(grid_rows):
    r = grid_rows
    m = r + 1
    s = (10 ** r - 1) // 9
    sum_x = s - m
    return math.comb(sum_x + m - 1, m - 1)

# 调用 solve
result = solve(inputs['grid_rows'])
print(result)