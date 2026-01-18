inputs = {'max_n': 2024}

def solve(max_n):
    if max_n <= 0:
        return 0
    q, r = divmod(max_n, 5)
    return q * 2 + (1 if r >= 2 else 0)

solve(2024)

# 调用 solve
result = solve(inputs['max_n'])
print(result)