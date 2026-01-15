inputs = {'R': 13}

def solve(R):
    r = 6
    OI2 = R*R - 2*R*r
    AI2 = R*R - OI2  # right angle at I implies AI^2 = AO^2 - OI^2
    return 3 * AI2

solve(13)

# 调用 solve
result = solve(inputs['R'])
print(result)