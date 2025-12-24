inputs = {'N': 601}

def solve(N):
    S = 300
    counts = {}
    for a in range(S + 1):
        for b in range(S - a + 1):
            c = S - a - b
            ab = a * b
            bc = b * c
            ca = c * a
            abc = a * b * c
            M = S * (ab + bc + ca) - 3 * abc
            counts[M] = counts.get(M, 0) + 1
    candidates = [m for m, cnt in counts.items() if cnt == N]
    return min(candidates) if candidates else None

solve(601)

# 调用 solve
result = solve(inputs['N'])
print(result)