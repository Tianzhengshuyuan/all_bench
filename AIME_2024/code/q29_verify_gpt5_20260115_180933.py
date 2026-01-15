inputs = {'CE': 104}

import math

def solve(CE):
    AB = 107.0
    BC = 16.0
    EF = 184.0

    DE = AB - CE
    half_BC = BC / 2.0

    rad = DE * (DE + EF) + half_BC ** 2
    s = math.sqrt(rad)
    FG = abs(s - half_BC)

    FG_int = round(FG)
    return int(FG_int) if abs(FG - FG_int) < 1e-9 else FG

solve(104)

# 调用 solve
result = solve(inputs['CE'])
print(result)