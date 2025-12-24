inputs = {'K': 809}

def solve(K):
    B = 2024
    m = 5
    q, r = divmod(B, m)

    # General counting over residues for n in [1..B]:
    # count[0] = q
    # count[a] = q+1 for a in {1..r}, and q for a in {r+1..m-1}
    # Let S be residues where Bob always wins.
    # If s = |S|, I0 = indicator(0 in S), and s1 = |S ∩ {1..r}|,
    # then K = sum_{res in S} count[res] = q*s + s1
    # Feasible range for s1:
    #   s_nonzero = s - I0 must be split between:
    #     - among r residues with count q+1: choose s1
    #     - among (m-1-r) residues with count q: choose s_nonzero - s1
    # So s1 ∈ [max(0, s_nonzero - (m-1-r)), min(r, s_nonzero)]
    for s in range(0, m + 1):
        for I0 in (0, 1):
            if I0 > s:
                continue
            s_nonzero = s - I0
            s1_min = max(0, s_nonzero - (m - 1 - r))
            s1_max = min(r, s_nonzero)
            s1 = K - q * s
            if s1_min <= s1 <= s1_max:
                return 10 * I0 + s

    # Fallback: compute S via game DP and return N from definition
    moves = (1, 4)
    M = 100
    win = [False] * (M + 1)  # win[n] = True if Alice (to move) wins with n tokens
    for n in range(1, M + 1):
        win[n] = any(n - mv >= 0 and not win[n - mv] for mv in moves)

    S = set()
    for residue in range(m):
        start = residue if residue != 0 else m  # positive n
        ok = True
        for n in range(start, M + 1, m):
            if win[n]:
                ok = False
                break
        if ok:
            S.add(residue)

    I0 = 1 if 0 in S else 0
    return 10 * I0 + len(S)

solve(809)

# 调用 solve
result = solve(inputs['K'])
print(result)