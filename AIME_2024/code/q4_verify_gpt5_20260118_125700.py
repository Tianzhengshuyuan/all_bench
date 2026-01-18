inputs = {'N': 2024}

def solve(N):
    if N <= 0:
        return 0
    q, r = divmod(N, 5)
    return 2 * q + (1 if r >= 2 else 0)

solve(2024)

# 调用 solve
result = solve(inputs['N'])
print(result)