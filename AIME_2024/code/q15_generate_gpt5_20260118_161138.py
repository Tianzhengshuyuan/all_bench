inputs = {'turns': 10}

def solve(turns):
    import math
    n = 8  # grid size: 8x8, so 8 rights and 8 ups
    t = int(turns)
    if t < 1 or t > 2 * n - 1:
        return 0
    # number of segments of R and U when starting with R
    seg_R = (t + 2) // 2  # ceil((t+1)/2)
    seg_U = (t + 1) // 2  # floor((t+1)/2)
    if seg_R > n or seg_U > n:
        return 0
    return 2 * math.comb(n - 1, seg_R - 1) * math.comb(n - 1, seg_U - 1)

# 调用 solve
result = solve(inputs['turns'])
print(result)