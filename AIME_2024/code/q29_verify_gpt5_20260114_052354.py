inputs = {'fg_length': 17}

def solve(fg_length):
    AB = 107.0
    BC = 16.0
    EF = 184.0
    disc = EF * EF + 4.0 * fg_length * (fg_length + BC)
    x = (-EF + disc ** 0.5) / 2.0  # DE
    CE = AB - x
    if abs(CE - round(CE)) < 1e-9:
        return int(round(CE))
    return CE

solve(fg_length)

# 调用 solve
result = solve(inputs['fg_length'])
print(result)