inputs = {'N': 601}

def solve(N):
    total = 300
    counts = {}
    for a in range(total + 1):
        for b in range(total - a + 1):
            c = total - a - b
            ab = a * b
            bc = b * c
            ca = c * a
            M = 300 * (ab + bc + ca) - 3 * (a * b * c)
            counts[M] = counts.get(M, 0) + 1
    candidates = [m for m, cnt in counts.items() if cnt == N]
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]
    return min(candidates)

solve(601)

# 调用 solve
result = solve(inputs['N'])
print(result)