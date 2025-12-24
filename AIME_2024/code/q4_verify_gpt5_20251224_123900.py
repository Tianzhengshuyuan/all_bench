inputs = {'K': 809}

def solve(K):
    B = 2024
    m = 5
    q, r = divmod(B, m)
    for s in range(0, m + 1):
        for I0 in (0, 1):
            if I0 > s:
                continue
            s_nonzero = s - I0
            s1 = K - q * s
            if 0 <= s1 <= r and 0 <= s_nonzero - s1 <= (m - 1 - r):
                return 10 * I0 + s
    # Fallback via DP to determine S and compute N
    moves = (1, 4)
    M = 10 * m
    win = [False] * (M + 1)
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