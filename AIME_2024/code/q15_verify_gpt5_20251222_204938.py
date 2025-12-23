inputs = {'turns': 4}

from math import comb

def solve(turns):
    R = U = 8
    if turns < 1:
        return 0
    seg = turns + 1
    r_big = (seg + 1) // 2  # number of segments of the starting direction
    r_small = seg // 2      # number of segments of the other direction
    if r_big > R or r_small > U:
        return 0
    return 2 * comb(R - 1, r_big - 1) * comb(U - 1, r_small - 1)

solve(turns)

# 调用 solve
result = solve(inputs['turns'])
print(result)