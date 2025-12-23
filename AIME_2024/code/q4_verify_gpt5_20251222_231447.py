inputs = {'limit': 2024}

def solve(limit):
    if limit <= 0:
        return 0
    moves = (1, 4)
    dp = [False] * (limit + 1)  # dp[n] = True if current player has a winning strategy with n tokens
    count_losing = 0
    for n in range(1, limit + 1):
        dp[n] = any(n >= m and not dp[n - m] for m in moves)
        if not dp[n]:
            count_losing += 1
    return count_losing

solve(2024)

# 调用 solve
result = solve(inputs['limit'])
print(result)