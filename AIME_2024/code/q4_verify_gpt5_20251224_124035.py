inputs = {'K': 809}

def solve(K):
    B = 2024
    m = 5
    moves = (1, 4)

    # Determine S via game DP
    M = 100
    win = [False] * (M + 1)  # win[n] = True if Alice (to move) wins with n tokens
    for n in range(1, M + 1):
        win[n] = any(n - mv >= 0 and not win[n - mv] for mv in moves)

    S = set()
    for res in range(m):
        start = res if res != 0 else m  # positive n
        ok = True
        for n in range(start, M + 1, m):
            if win[n]:
                ok = False
                break
        if ok:
            S.add(res)

    I0 = 1 if 0 in S else 0
    N = 10 * I0 + len(S)

    # Verify against given K by counting up to B
    def count_up_to_B(res):
        first = res if res != 0 else m
        if first > B:
            return 0
        return (B - first) // m + 1

    Kcalc = sum(count_up_to_B(res) for res in S)
    if Kcalc == K:
        return N

    # Fallback: deduce (I0, |S|) from K and residue counts alone
    q, rem = divmod(B, m)
    for s in range(0, m + 1):
        for I in (0, 1):
            if I > s:
                continue
            s_nonzero = s - I
            s1 = K - q * s
            if 0 <= s1 <= rem and 0 <= s_nonzero - s1 <= (m - 1 - rem):
                return 10 * I + s

    return N

solve(809)

# 调用 solve
result = solve(inputs['K'])
print(result)