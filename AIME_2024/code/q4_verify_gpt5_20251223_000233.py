inputs = {'limit': 2024}

def solve(limit):
    if limit <= 0:
        return 0
    return (limit // 5) + max(0, (limit - 2) // 5 + 1)

solve(2024)

# 调用 solve
result = solve(inputs['limit'])
print(result)