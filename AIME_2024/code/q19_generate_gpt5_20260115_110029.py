inputs = {'r': 40}

def solve(r):
    R = 13
    OI2 = R * (R - 2 * r)
    AI2 = R * R - OI2
    return 3 * AI2

result = solve(6)

# 调用 solve
result = solve(inputs['r'])
print(result)