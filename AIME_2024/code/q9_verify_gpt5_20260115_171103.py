inputs = {'xy': 25}

def solve(xy):
    import math
    if xy is None or xy <= 0:
        return None
    N = 2 * math.sqrt(xy)
    if abs(N - round(N)) < 1e-9:
        return int(round(N))
    return N

xy = 25
solve(xy)

# 调用 solve
result = solve(inputs['xy'])
print(result)