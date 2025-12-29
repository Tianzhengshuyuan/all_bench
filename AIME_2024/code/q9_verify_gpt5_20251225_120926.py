inputs = {'xy': 25}

def solve(xy):
    N = 2 * (xy ** 0.5)
    r = round(N)
    return int(r) if abs(N - r) < 1e-12 else N

solve(25)

# 调用 solve
result = solve(inputs['xy'])
print(result)