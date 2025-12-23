inputs = {'FG_length': 17}

def solve(FG_length):
    AB = 107.0
    BC = 16.0
    EF = 184.0
    half_BC = BC / 2.0
    half_EF = EF / 2.0
    OP = half_BC + FG_length
    rhs = OP * OP + half_EF * half_EF - half_BC * half_BC
    x = (rhs ** 0.5) - half_EF  # DE
    CE = AB - x
    return int(round(CE)) if abs(CE - round(CE)) < 1e-9 else CE

FG_length = 17
solve(FG_length)

# 调用 solve
result = solve(inputs['FG_length'])
print(result)