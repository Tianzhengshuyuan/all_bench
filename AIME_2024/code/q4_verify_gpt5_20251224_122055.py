inputs = {'K': 809}

def solve(K):
    B = 2024
    moves = (1, 4)

    # Compute winning states for Alice up to a sufficient bound to see periodicity
    M = 60
    win = [False] * (M + 1)  # win[n] = True if Alice (to move) wins with n tokens
    for n in range(1, M + 1):
        win[n] = any(n - mv >= 0 and not win[n - mv] for mv in moves)

    # Determine S: residues r mod 5 such that all positive n ≡ r (mod 5) are losing for Alice
    S = set()
    for r in range(5):
        ok = True
        start = r if r != 0 else 5  # only check positive n
        for n in range(start, M + 1, 5):
            if win[n]:
                ok = False
                break
        if ok:
            S.add(r)

    I0 = 1 if 0 in S else 0
    N = 10 * I0 + len(S)
    return N

solve(809)

# 调用 solve
result = solve(inputs['K'])
print(result)