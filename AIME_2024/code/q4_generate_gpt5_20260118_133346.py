inputs = {'limit': 2089}

def solve(limit):
    if limit < 1:
        return 0
    count0 = limit // 5
    count2 = 0 if limit < 2 else 1 + (limit - 2) // 5
    return count0 + count2

solve(2024)

# 调用 solve
result = solve(inputs['limit'])
print(result)