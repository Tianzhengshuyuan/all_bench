inputs = {'CE': 104}

def solve(CE):
    AB = 107
    CD = AB
    DE = CD - CE
    return DE

solve(CE)

# 调用 solve
result = solve(inputs['CE'])
print(result)