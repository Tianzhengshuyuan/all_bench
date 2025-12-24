inputs = {'N': 601}

def solve(N):
    counts_M = {}
    for a in range(301):
        for b in range(301 - a):
            c = 300 - a - b
            M = a * a * (300 - a) + b * b * (300 - b) + c * c * (300 - c)
            counts_M[M] = counts_M.get(M, 0) + 1
    candidates = [M for M, cnt in counts_M.items() if cnt == N]
    return min(candidates) if candidates else None

solve(601)

# 调用 solve
result = solve(inputs['N'])
print(result)