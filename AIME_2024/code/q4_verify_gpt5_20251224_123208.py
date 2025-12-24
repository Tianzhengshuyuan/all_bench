inputs = {'K': 809}

def solve(K):
    B = 2024
    m = 5
    moves = (1, 4)

    # Compute winning states for Alice
    M = 25
    win = [False] * (M + 1)
    for n in range(1, M + 1):
        win[n] = any(n - mv >= 0 and not win[n - mv] for mv in moves)

    # Determine S: residues r mod 5 such that all positive n ≡ r (mod 5) are losing for Alice
    S = set()
    for r in range(m):
        start = r if r != 0 else m
        ok = True
        for n in range(start, M + 1, m):
            if win[n]:
                ok = False
                break
        if ok:
            S.add(r)

    I0 = 1 if 0 in S else 0
    N = 10 * I0 + len(S)

    # Verify with given K (counts up to B)
    counts = []
    for r in range(m):
        first = r if r != 0 else m
        if first > B:
            cnt = 0
        else:
            cnt = (B - first) // m + 1
        counts.append(cnt)
    Kcalc = sum(counts[r] for r in S)
    if Kcalc == K:
        return N

    # Fallback: derive (I0, |S|) from K and residue counts alone
    q, r = divmod(B, m)
    for s in range(0, m + 1):
        for I in (0, 1):
            if I > s:
                continue
            s_nonzero = s - I
            s1 = K - q * s
            if 0 <= s1 <= r and 0 <= s_nonzero - s1 <= (m - 1 - r):
                return 10 * I + s

    return N

solve(809)

# 调用 solve
result = solve(inputs['K'])
print(result)