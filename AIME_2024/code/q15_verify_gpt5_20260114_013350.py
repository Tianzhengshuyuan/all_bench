inputs = {'turns': 4}

from math import comb

def solve(turns):
    R_total = 8
    U_total = 8
    S = turns + 1
    total = 0
    for start_is_R in (True, False):
        if start_is_R:
            r_segments = (S + 1) // 2
            u_segments = S // 2
        else:
            r_segments = S // 2
            u_segments = (S + 1) // 2
        if 1 <= r_segments <= R_total and 1 <= u_segments <= U_total:
            total += comb(R_total - 1, r_segments - 1) * comb(U_total - 1, u_segments - 1)
    return total

solve(4)

# 调用 solve
result = solve(inputs['turns'])
print(result)