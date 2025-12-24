inputs = {'N': 601}

def solve(N):
    from collections import defaultdict
    counts = defaultdict(int)
    for a in range(301):
        for b in range(301 - a):
            c = 300 - a - b
            t = (100 - a) * (100 - b) * (100 - c)
            counts[t] += 1
    candidates = [t for t, cnt in counts.items() if cnt == N]
    if not candidates:
        return None
    best_t = min(candidates, key=lambda x: (abs(x), x))
    M = 6000000 + 3 * best_t
    return M

solve(601)

# 调用 solve
result = solve(inputs['N'])
print(result)