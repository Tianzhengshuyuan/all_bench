inputs = {'K': 809}

def solve(K):
    m = 5
    T = 2024
    q, r = divmod(T, m)
    # Try to deduce |S| (x) and I0 (y) from K when r == m-1
    ans = None
    if r == m - 1:
        for x in range(0, m + 1):
            y = (q + 1) * x - K
            if y in (0, 1) and y <= x:
                ans = 10 * y + x
                break
    if ans is None:
        # Fallback: compute S via DP up to T
        moves = (1, 4)
        dp = [False] * (T + 1)  # False = losing for player to move (Bob wins)
        for n in range(1, T + 1):
            dp[n] = any(n >= mv and not dp[n - mv] for mv in moves)
        S = set()
        for rr in range(m):
            if all(not dp[n] for n in range(1, T + 1) if n % m == rr):
                S.add(rr)
        ans = 10 * (1 if 0 in S else 0) + len(S)
    return ans

solve(809)

# 调用 solve
result = solve(inputs['K'])
print(result)