inputs = {'K': 809}

def solve(K):
    B = 2024
    m = 5
    q, r = divmod(B, m)  # q=404, r=4
    # For B=2024: counts per residue are c[0]=q, c[1..4]=q+1
    # So K = (q+1)*|S| - I0
    for I0 in (0, 1):
        for s in range(I0, m + 1):
            if (q + 1) * s - I0 == K:
                return 10 * I0 + s
    # Fallback via game DP (should not be needed for valid K)
    max_check = 25
    win = [False] * (max_check + 1)  # win[n]: Alice wins with n coins
    for n in range(1, max_check + 1):
        win[n] = any(n - mv >= 0 and not win[n - mv] for mv in (1, 4))
    residues = {n % 5 for n in range(1, max_check + 1) if not win[n]}
    I0 = 1 if 0 in residues else 0
    s = len(residues)
    return 10 * I0 + s

solve(809)

# 调用 solve
result = solve(inputs['K'])
print(result)