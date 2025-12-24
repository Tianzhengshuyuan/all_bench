inputs = {'K': 809}

def solve(K):
    B = 2024
    m = 5

    # Count how many numbers in [1..B] fall into each residue class mod m
    counts = []
    for r in range(m):
        first = r if r != 0 else m  # smallest positive n ≡ r (mod m)
        if first > B:
            cnt = 0
        else:
            cnt = (B - first) // m + 1
        counts.append(cnt)

    candidates = set()
    for mask in range(1 << m):
        total = 0
        for r in range(m):
            if (mask >> r) & 1:
                total += counts[r]
        if total == K:
            I0 = 1 if (mask & 1) else 0
            s = bin(mask).count("1")
            candidates.add(10 * I0 + s)

    if candidates:
        return min(candidates)
    return None

solve(809)

# 调用 solve
result = solve(inputs['K'])
print(result)