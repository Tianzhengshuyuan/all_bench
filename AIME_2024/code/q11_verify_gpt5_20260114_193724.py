inputs = {'radius': 4}

import math

def solve(radius):
    r = float(radius)
    if r <= 0:
        return float('nan')
    A, B = 75.0, 117.0
    C, D = 96.0, 144.0
    p = A + C/(r*r)
    q = -B + D/(r*r)
    res = r * math.hypot(p, q)
    ir = round(res)
    return int(ir) if abs(res - ir) < 1e-9 else res

solve(4)

# 调用 solve
result = solve(inputs['radius'])
print(result)