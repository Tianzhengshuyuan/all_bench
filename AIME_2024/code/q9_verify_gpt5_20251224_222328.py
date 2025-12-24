inputs = {'xy': 25}

def solve(xy):
    import math
    return 2 * math.sqrt(xy)

solve(25)

# 调用 solve
result = solve(inputs['xy'])
print(result)