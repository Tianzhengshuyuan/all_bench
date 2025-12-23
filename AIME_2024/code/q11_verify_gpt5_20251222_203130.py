inputs = {'coef_z_real': 75}

import math

def solve(coef_z_real):
    c = float(coef_z_real)
    val = 4.0 * math.hypot(c + 6.0, 108.0)
    if abs(val - round(val)) < 1e-9:
        return int(round(val))
    return val

solve(75)

# 调用 solve
result = solve(inputs['coef_z_real'])
print(result)