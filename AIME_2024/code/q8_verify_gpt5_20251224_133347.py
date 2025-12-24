inputs = {'N': 601}

def solve(N):
    S = 300
    freq = {}
    for a in range(S + 1):
        for b in range(S - a + 1):
            c = S - a - b
            ab = a * b
            bc = b * c
            ca = c * a
            abc = a * b * c
            E = S * (ab + bc + ca) - 3 * abc
            freq[E] = freq.get(E, 0) + 1
    res = [M for M, cnt in freq.items() if cnt == N]
    if len(res) == 1:
        return res[0]
    return sorted(res)

solve(601)

# 调用 solve
result = solve(inputs['N'])
print(result)