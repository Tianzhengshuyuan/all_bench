inputs = {'fg_length': 17}

def solve(fg_length):
    import math
    AB = 107.0
    BC = 16.0
    EF = 184.0
    half_BC = BC / 2.0
    half_EF = EF / 2.0
    s = (half_BC + fg_length) ** 2 + half_EF ** 2 - half_BC ** 2
    s = max(s, 0.0)
    x = math.sqrt(s) - half_EF
    CE = AB - x
    if abs(round(CE) - CE) < 1e-9:
        return int(round(CE))
    return CE

solve(17)

# 调用 solve
result = solve(inputs['fg_length'])
print(result)