inputs = {'CE': 104}

def solve(CE):
    AB = 107
    BC = 16
    FG = 17
    x = AB - CE
    e = FG * (BC + FG) / x - x
    return int(round(e)) if abs(e - round(e)) < 1e-9 else e

solve(104)

# 调用 solve
result = solve(inputs['CE'])
print(result)