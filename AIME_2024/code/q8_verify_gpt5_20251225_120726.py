inputs = {'triples_count': 601}

def solve(triples_count):
    try:
        t = int(triples_count)
    except Exception:
        return None
    if t <= 0:
        return None
    diff = t - 1
    if diff % 6 != 0:
        return None
    N = diff // 6
    if N <= 0:
        return None
    return N

solve(601)

# 调用 solve
result = solve(inputs['triples_count'])
print(result)