inputs = {'num_triples': 601}

def solve(num_triples):
    total = 300
    counts = {}
    for a in range(total + 1):
        for b in range(total - a + 1):
            c = total - a - b
            ab = a * b
            bc = b * c
            ca = c * a
            abc = a * b * c
            S = 300 * (ab + bc + ca) - 3 * abc
            counts[S] = counts.get(S, 0) + 1
    candidates = [S for S, cnt in counts.items() if cnt == num_triples]
    if not candidates:
        return None
    return min(candidates)

solve(601)

# 调用 solve
result = solve(inputs['num_triples'])
print(result)