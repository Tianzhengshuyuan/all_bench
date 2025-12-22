inputs = {'circumradius': 13}

def solve(circumradius):
    R = circumradius
    r = 6
    OI2 = R * (R - 2 * r)
    AI2 = R * R - OI2
    return 3 * AI2

result = solve(13)

# 调用 solve
result = solve(inputs['circumradius'])
print(result)