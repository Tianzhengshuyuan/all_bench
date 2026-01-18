inputs = {'r': 4}

def solve(r):
    A = 75 + 117j
    B = 96 + 144j
    r = float(r)
    return abs(r*A + B.conjugate()/r)

solve(4)

# 调用 solve
result = solve(inputs['r'])
print(result)