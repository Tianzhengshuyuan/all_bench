inputs = {'K': 809}

def solve(K):
    B = 2024
    m = 5
    q, rem = divmod(B, m)
    # Counts for residues among 1..B:
    # residue 0 has q occurrences; residues 1..rem have q+1; residues rem+1..m-1 have q.
    # Let S be the residue set where Bob always wins. If s = |S|, I0 = indicator(0 in S),
    # and s1 = |S ∩ {1..rem}|, then K = q*s + s1 with constraints:
    # 0 <= s1 <= rem and 0 <= (s - I0) - s1 <= (m - 1 - rem).
    for s in range(0, m + 1):
        for I0 in (0, 1):
            if I0 > s:
                continue
            s_nonzero = s - I0
            s1 = K - q * s
            if 0 <= s1 <= rem and 0 <= s_nonzero - s1 <= (m - 1 - rem):
                return 10 * I0 + s
    # Fallback via game DP (shouldn't be needed for consistent K)
    moves = (1, 4)
    M = 100
    win = [False] * (M + 1)  # win[n]: True if Alice (to move) wins with n tokens
    for n in range(1, M + 1):
        win[n] = any(n - mv >= 0 and not win[n - mv] for mv in moves)
    S = set()
    for res in range(m):
        start = res if res != 0 else m
        ok = True
        for n in range(start, M + 1, m):
            if win[n]:
                ok = False
                break
        if ok:
            S.add(res)
    I0 = 1 if 0 in S else 0
    return 10 * I0 + len(S)

solve(809)

# 调用 solve
result = solve(inputs['K'])
print(result)