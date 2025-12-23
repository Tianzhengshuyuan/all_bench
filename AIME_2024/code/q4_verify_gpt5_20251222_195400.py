inputs = {'limit': 2024}

def solve(limit):
    if limit <= 0:
        return 0
    count0 = limit // 5
    count2 = (limit - 2) // 5 + 1 if limit >= 2 else 0
    return count0 + count2

solve(2024)

# 调用 solve
result = solve(inputs['limit'])
print(result)