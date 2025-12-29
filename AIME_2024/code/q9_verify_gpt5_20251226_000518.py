inputs = {'xy': 25}

def solve(xy):
    import math
    if xy < 0:
        return None
    N = 2 * math.sqrt(xy)
    n_int = int(round(N))
    if abs(N - n_int) < 1e-12:
        return n_int
    return N

solve(25)

# 调用 solve
result = solve(inputs['xy'])
print(result)