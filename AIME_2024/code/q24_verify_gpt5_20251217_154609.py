inputs = {'sum': 30}

from collections import Counter

def solve(sum):
    S = sum

    def partitions(total, start=1):
        if total == 0:
            yield []
            return
        for x in range(start, total + 1):
            for rest in partitions(total - x, x):
                yield [x] + rest

    candidates = []
    for arr in partitions(S, 1):
        n = len(arr)
        if n % 2 == 1:
            continue
        c = Counter(arr)
        if 9 not in c:
            continue
        max_freq = max(c.values())
        modes = [v for v, f in c.items() if f == max_freq]
        if len(modes) != 1 or modes[0] != 9:
            continue
        m1, m2 = arr[n // 2 - 1], arr[n // 2]
        if (m1 + m2) % 2 != 0:
            continue
        median = (m1 + m2) // 2
        if median in c:
            continue
        sumsq = 0
        for x in arr:
            sumsq += x * x
        candidates.append(sumsq)

    if len(candidates) == 1:
        return candidates[0]
    return candidates[0] if candidates else None

# 调用 solve
result = solve(inputs['sum'])
print(result)