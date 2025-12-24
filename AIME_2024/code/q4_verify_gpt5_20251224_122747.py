inputs = {'K': 809}

def solve(K):
    nmax = 2024
    M = 5
    counts = []
    for r in range(M):
        first = r if r != 0 else M
        if first > nmax:
            cnt = 0
        else:
            cnt = (nmax - first) // M + 1
        counts.append(cnt)
    for mask in range(1 << M):
        total = 0
        for r in range(M):
            if (mask >> r) & 1:
                total += counts[r]
        if total == K:
            b = 1 if (mask & 1) else 0  # whether residue 0 is in S
            m = bin(mask).count("1")    # |S|
            return 10 * b + m
    return None

solve(809)

# 调用 solve
result = solve(inputs['K'])
print(result)