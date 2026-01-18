inputs = {'n': 303}

def solve(n):
    if n % 3 != 0:
        return 0
    return 2 * n + 1

solve(300)

# 调用 solve
result = solve(inputs['n'])
print(result)