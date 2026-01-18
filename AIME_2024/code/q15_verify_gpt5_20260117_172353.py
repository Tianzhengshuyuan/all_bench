inputs = {'change_count': 4}

from math import comb

def solve(change_count):
    nR = 8
    nU = 8
    t = change_count
    runs = t + 1
    r_runs = (runs + 1) // 2
    u_runs = runs // 2
    if r_runs < 1 or u_runs < 1:
        return 0
    if r_runs > nR or u_runs > nU:
        return 0
    return 2 * comb(nR - 1, r_runs - 1) * comb(nU - 1, u_runs - 1)

solve(4)

# 调用 solve
result = solve(inputs['change_count'])
print(result)