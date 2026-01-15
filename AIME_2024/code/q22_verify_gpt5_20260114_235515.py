inputs = {'side1': 200}

def solve(side1):
    a = side1
    b = side1 * 240 / 200
    c = side1 * 300 / 200
    return c / (1 + c/a + c/b)

solve(side1)

# 调用 solve
result = solve(inputs['side1'])
print(result)