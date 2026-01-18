inputs = {'r': 4}

def solve(r):
    import math
    R = abs(r)
    if R == 0:
        return float('nan')
    ax, ay = 75.0, 117.0
    bx, by = 96.0, 144.0
    real_part = R * ax + bx / R
    imag_part = R * ay - by / R
    return math.hypot(real_part, imag_part)

solve(4)

# 调用 solve
result = solve(inputs['r'])
print(result)