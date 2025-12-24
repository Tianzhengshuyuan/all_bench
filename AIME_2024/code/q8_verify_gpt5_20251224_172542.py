inputs = {'num_triples': 601}

def solve(num_triples):
    S = 300
    const = 6000000
    counts = {}
    for a in range(S + 1):
        x = a - 100
        for b in range(S - a + 1):
            y = b - 100
            z = -x - y  # since (a-100)+(b-100)+(c-100)=0
            E = const - 3 * x * y * z
            counts[E] = counts.get(E, 0) + 1
    candidates = [E for E, cnt in counts.items() if cnt == num_triples]
    if not candidates:
        return None
    return min(candidates)

solve(601)

# 调用 solve
result = solve(inputs['num_triples'])
print(result)