inputs = {'N': 601}

def solve(N):
    T = 300
    counts = {}
    for a in range(T + 1):
        for b in range(T - a + 1):  # include boundary so c can be 0
            c = T - a - b
            M = a * a * (T - a) + b * b * (T - b) + c * c * (T - c)
            counts[M] = counts.get(M, 0) + 1
    candidates = [m for m, cnt in counts.items() if cnt == N]
    return min(candidates) if candidates else None

solve(601)

# 调用 solve
result = solve(inputs['N'])
print(result)