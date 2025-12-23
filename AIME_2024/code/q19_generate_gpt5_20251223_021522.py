inputs = {'R': 25}

def solve(R):
    r = 6
    oi2 = R * (R - 2 * r)
    ai2 = R * R - oi2
    return 3 * ai2

solve(13)

# 调用 solve
result = solve(inputs['R'])
print(result)