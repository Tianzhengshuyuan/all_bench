inputs = {'N': 601}

def solve(N):
    T = 300
    counts_M = {}
    for a in range(T + 1):
        for b in range(T - a + 1):
            c = T - a - b
            M = a * a * (T - a) + b * b * (T - b) + c * c * (T - c)
            counts_M[M] = counts_M.get(M, 0) + 1
    candidates = [m for m, cnt in counts_M.items() if cnt == N]
    return min(candidates) if candidates else None

solve(601)

# 调用 solve
result = solve(inputs['N'])
print(result)