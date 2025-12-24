inputs = {'K': 809}

def solve(K):
    M = 5
    Nmax = 2024

    def count_residue_upto(N, m, r):
        if r == 0:
            return N // m
        if N < r:
            return 0
        return (N - r) // m + 1

    counts = [count_residue_upto(Nmax, M, r) for r in range(M)]

    candidates = set()
    for mask in range(1 << M):
        total = 0
        for r in range(M):
            if (mask >> r) & 1:
                total += counts[r]
        if total == K:
            I0 = 1 if (mask & 1) else 0
            s = bin(mask).count("1")
            candidates.add(10 * I0 + s)

    if candidates:
        # Should be unique for valid K; pick the unique or the minimal if multiple
        return min(candidates)
    return None

solve(809)

# 调用 solve
result = solve(inputs['K'])
print(result)