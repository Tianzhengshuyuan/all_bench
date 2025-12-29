inputs = {'num_triples': 601}

def solve(num_triples):
    S = 300
    counts = {}
    for a in range(S + 1):
        Sa = S - a
        termA = a * a * Sa
        for b in range(Sa + 1):
            c = Sa - b
            E = termA + b * b * (S - b) + c * c * (S - c)
            counts[E] = counts.get(E, 0) + 1
    candidates = [N for N, cnt in counts.items() if cnt == num_triples]
    return min(candidates) if candidates else -1

solve(601)

# 调用 solve
result = solve(inputs['num_triples'])
print(result)