inputs = {'limit': 2024}

def solve(limit: int) -> int:
    if limit <= 0:
        return 0
    moves = (1, 4)
    dp = [False] * (limit + 1)  # dp[n] = True if position with n tokens is winning for player to move
    for n in range(1, limit + 1):
        dp[n] = any(n - m >= 0 and not dp[n - m] for m in moves)
    return sum(1 for n in range(1, limit + 1) if not dp[n])

# 调用 solve
result = solve(inputs['limit'])
print(result)