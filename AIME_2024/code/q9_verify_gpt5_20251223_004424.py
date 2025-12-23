inputs = {'k': 10}

def solve(k):
    a = k * k
    if isinstance(k, int) and a % 4 == 0:
        return a // 4
    return a / 4

solve(10)

# 调用 solve
result = solve(inputs['k'])
print(result)