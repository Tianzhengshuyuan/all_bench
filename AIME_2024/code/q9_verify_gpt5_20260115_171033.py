inputs = {'xy': 25}

def solve(xy):
    import math
    return 2 * math.sqrt(xy)

xy = 25
solve(xy)

# 调用 solve
result = solve(inputs['xy'])
print(result)