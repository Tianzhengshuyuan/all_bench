inputs = {'length': 16}

from math import comb

def solve(length):
    if length % 2 != 0:
        return 0
    N = length // 2
    if N < 3:
        return 0
    return 2 * comb(N - 1, 2) * comb(N - 1, 1)

solve(16)

# 调用 solve
result = solve(inputs['length'])
print(result)