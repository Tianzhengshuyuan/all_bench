inputs = {'r': 19}

def solve(r):
    R = 13
    OI_sq = R * (R - 2 * r)
    AI_sq = R * R - OI_sq
    return 3 * AI_sq

solve(6)

# 调用 solve
result = solve(inputs['r'])
print(result)