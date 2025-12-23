inputs = {'limit': 2024}

def solve(limit):
    if limit <= 0:
        return 0
    q, r = divmod(limit, 5)
    return q * 2 + (1 if r >= 2 else 0)

solve(2024)

# 调用 solve
result = solve(inputs['limit'])
print(result)