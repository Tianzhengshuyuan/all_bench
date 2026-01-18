inputs = {'R': 22}

def solve(R):
    r = 6
    OI2 = R * R - 2 * R * r
    AI2 = R * R - OI2
    return 3 * AI2

# 调用 solve
result = solve(inputs['R'])
print(result)