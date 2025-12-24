inputs = {'N': 601}

def solve(N):
    counts = {}
    for a in range(301):
        for b in range(301 - a):
            c = 300 - a - b
            ab = a * b
            bc = b * c
            ca = c * a
            abc = a * b * c
            M = 300 * (ab + bc + ca) - 3 * abc
            counts[M] = counts.get(M, 0) + 1
    candidates = [M for M, cnt in counts.items() if cnt == N]
    return min(candidates) if candidates else None

solve(601)

# 调用 solve
result = solve(inputs['N'])
print(result)