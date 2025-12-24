inputs = {'xy': 25}

def solve(xy):
    import math
    N = 2 * math.sqrt(xy)
    # Return integer if it's effectively an integer
    r = round(N)
    return r if abs(N - r) < 1e-12 else N

solve(25)

# 调用 solve
result = solve(inputs['xy'])
print(result)