inputs = {'path_length': 16}

import math

def solve(path_length):
    n = path_length // 2
    c1 = math.comb(n - 1, 2)
    c2 = math.comb(n - 1, 1)
    return 2 * c1 * c2

# 调用 solve
result = solve(inputs['path_length'])
print(result)