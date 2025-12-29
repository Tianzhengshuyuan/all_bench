inputs = {'triples_count': 601}

def solve(triples_count):
    try:
        t = int(triples_count)
    except Exception:
        return None
    if t <= 0:
        return None
    if (t - 1) % 6 != 0:
        return None
    N = (t - 1) // 6
    if N <= 0:
        return None
    return N

solve(triples_count)

# 调用 solve
result = solve(inputs['triples_count'])
print(result)