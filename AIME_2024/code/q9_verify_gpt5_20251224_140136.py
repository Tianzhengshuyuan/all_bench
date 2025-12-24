inputs = {'xy': 25}

def solve(xy):
    import math
    if xy < 0:
        return float('nan')
    N = 2 * math.sqrt(xy)
    rn = round(N)
    return int(rn) if abs(N - rn) < 1e-12 else N

solve(25)

# 调用 solve
result = solve(inputs['xy'])
print(result)