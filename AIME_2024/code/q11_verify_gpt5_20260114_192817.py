inputs = {'r': 4}

def solve(r):
    import math
    if r <= 0:
        raise ValueError("r must be positive.")
    A, B = 75.0, 117.0
    C, D = 96.0, 144.0
    p = A * r + C / r
    q = -B * r + D / r
    val = math.hypot(p, q)
    iv = round(val)
    if abs(val - iv) < 1e-9:
        return int(iv)
    return val

solve(4)

# 调用 solve
result = solve(inputs['r'])
print(result)