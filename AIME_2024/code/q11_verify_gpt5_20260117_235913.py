inputs = {'numerator_real': 96}

import math

def solve(numerator_real):
    A = 75.0
    B = 117.0
    D = 144.0
    r = 4.0

    u1 = r * A
    u2 = r * B
    v1 = numerator_real / r
    v2 = D / r

    P = u1 + v1
    Q = -u2 + v2

    val = math.hypot(P, Q)
    rv = round(val)
    return int(rv) if abs(val - rv) < 1e-9 else val

solve(96)

# 调用 solve
result = solve(inputs['numerator_real'])
print(result)