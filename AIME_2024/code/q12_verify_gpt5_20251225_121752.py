inputs = {'ways': 45}

def solve(ways):
    import math
    D = 8 * ways + 1
    s = math.isqrt(D)
    if s * s != D:
        return None
    if (s - 3) % 2 != 0:
        return None
    return (s - 3) // 2

solve(45)

# 调用 solve
result = solve(inputs['ways'])
print(result)