inputs = {'r': 4}

def solve(r):
    import math
    if r <= 0:
        raise ValueError("r must be positive.")
    a1, a2 = 75.0, 117.0
    b1, b2 = 96.0, 144.0
    x = a1 * r + b1 / r
    y = a2 * r - b2 / r
    return math.hypot(x, y)

solve(4)

# 调用 solve
result = solve(inputs['r'])
print(result)