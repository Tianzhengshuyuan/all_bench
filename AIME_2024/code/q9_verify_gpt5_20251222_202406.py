inputs = {'k': 10}

def solve(k):
    num = k * k
    if isinstance(num, int) and num % 4 == 0:
        return num // 4
    return num / 4

solve(10)

# 调用 solve
result = solve(inputs['k'])
print(result)