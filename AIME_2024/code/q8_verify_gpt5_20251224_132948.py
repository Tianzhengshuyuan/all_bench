inputs = {'N': 601}

def solve(N):
    T = 300
    counts = {}
    for a in range(T + 1):
        for b in range(T - a + 1):
            c = T - a - b
            S = T * (a * b + b * c + c * a) - 3 * a * b * c
            counts[S] = counts.get(S, 0) + 1
    candidates = [M for M, cnt in counts.items() if cnt == N]
    if not candidates:
        return None
    return min(candidates)

solve(601)

# 调用 solve
result = solve(inputs['N'])
print(result)