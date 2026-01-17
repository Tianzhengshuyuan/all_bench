inputs = {'ways': 45}

def solve(ways):
    def count_triples(S):
        cnt = 0
        for a in range(10):
            for b in range(10):
                c = S - a - b
                if 0 <= c <= 9:
                    cnt += 1
        return cnt

    candidates = []
    for S in range(28):  # a+b+c ranges from 0 to 27
        if count_triples(S) == ways:
            candidates.append(9 * S + 27)
    if not candidates:
        return None
    return min(candidates)

solve(45)

# 调用 solve
result = solve(inputs['ways'])
print(result)