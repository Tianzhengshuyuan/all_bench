inputs = {'r': 4}

def solve(r):
    R = abs(r)
    if R == 0:
        return float('nan')
    A = 75 + 117j
    B = 96 + 144j
    return abs(R * A + B.conjugate() / R)

solve(4)

# 调用 solve
result = solve(inputs['r'])
print(result)