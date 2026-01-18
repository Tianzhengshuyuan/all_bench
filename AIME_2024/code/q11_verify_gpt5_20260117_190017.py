inputs = {'r': 4}

def solve(r):
    import math
    R = abs(float(r))
    if R == 0.0:
        return float('nan')
    ax, ay = 75.0, 117.0
    bx, by = 96.0, 144.0
    real = R * ax + bx / R
    imag = R * ay - by / R
    val = math.hypot(real, imag)
    if abs(val - round(val)) < 1e-12:
        return int(round(val))
    return val

solve(4)

# 调用 solve
result = solve(inputs['r'])
print(result)