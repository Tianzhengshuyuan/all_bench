inputs = {'turns': 4}

from math import comb

def solve(turns):
    R = U = 8
    if turns < 1:
        return 0
    seg = turns + 1

    # Case 1: start with R
    r1 = (seg + 1) // 2
    u1 = seg // 2
    count1 = comb(R - 1, r1 - 1) * comb(U - 1, u1 - 1) if r1 <= R and u1 <= U else 0

    # Case 2: start with U
    r2 = seg // 2
    u2 = (seg + 1) // 2
    count2 = comb(R - 1, r2 - 1) * comb(U - 1, u2 - 1) if r2 <= R and u2 <= U else 0

    return count1 + count2

turns = 4
solve(turns)

# 调用 solve
result = solve(inputs['turns'])
print(result)