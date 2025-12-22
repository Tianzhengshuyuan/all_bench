inputs = {'path_length': 16}

from math import comb

def solve(path_length):
    if path_length % 2 != 0 or path_length <= 0:
        return 0
    N = path_length // 2
    if N < 3:
        return 0
    return 2 * comb(N - 1, 2) * comb(N - 1, 1)

solve(16)

# 调用 solve
result = solve(inputs['path_length'])
print(result)