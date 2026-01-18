inputs = {'max_n': 1928}

def solve(max_n):
    if max_n <= 0:
        return 0
    moves = (1, 4)
    dp = [False] * (max_n + 1)  # False: losing for current player; True: winning
    count_losing = 0
    for n in range(1, max_n + 1):
        dp[n] = any(n >= m and not dp[n - m] for m in moves)
        if not dp[n]:
            count_losing += 1
    return count_losing

solve(2024)

# 调用 solve
result = solve(inputs['max_n'])
print(result)