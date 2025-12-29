inputs = {'ways': 45}

def solve(ways):
    counts = [0] * 28  # sums from 0 to 27
    for a in range(10):
        for b in range(10):
            for c in range(10):
                counts[a + b + c] += 1
    candidates = [s for s, cnt in enumerate(counts) if cnt == ways]
    if not candidates:
        return None
    s = min(candidates)
    return 9 * s + 27

solve(45)

# 调用 solve
result = solve(inputs['ways'])
print(result)