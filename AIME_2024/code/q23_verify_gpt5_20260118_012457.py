inputs = {'a': 20}

def solve(a):
    b = 24
    return 4 * a * b / (b - a)

solve(20)

# 调用 solve
result = solve(inputs['a'])
print(result)