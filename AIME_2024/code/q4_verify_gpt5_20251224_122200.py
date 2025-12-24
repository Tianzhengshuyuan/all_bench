inputs = {'K': 809}

def solve(K):
    B = 2024
    m = 5
    q, r = divmod(B, m)  # q=404, r=4 for B=2024

    # For n in [1..B], counts per residue:
    # count[0] = q, and for a in {1..r} count[a] = q+1, for a in {r+1..4} count[a] = q
    # Here r=4, so residues 1..4 appear q+1 times, residue 0 appears q times.
    # If S is the set of residues where Bob always wins, then:
    # K = sum_{res in S} count[res] = I0*q + (|S|-I0)*(q+1) = (q+1)*|S| - I0
    for s in range(0, m + 1):
        for I0 in (0, 1):
            if I0 <= s and (q + 1) * s - I0 == K:
                return 10 * I0 + s

    # If K is not consistent with any (I0, |S|), fall back to computing S from game DP
    moves = (1, 4)
    M = 100
    win = [False] * (M + 1)  # win[n] = True if Alice to move wins with n tokens
    for n in range(1, M + 1):
        win[n] = any(n - mv >= 0 and not win[n - mv] for mv in moves)

    S = set()
    for rres in range(m):
        start = rres if rres != 0 else m
        ok = True
        for n in range(start, M + 1, m):
            if win[n]:
                ok = False
                break
        if ok:
            S.add(rres)

    I0 = 1 if 0 in S else 0
    return 10 * I0 + len(S)

solve(809)

# 调用 solve
result = solve(inputs['K'])
print(result)