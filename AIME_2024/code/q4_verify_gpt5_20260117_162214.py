inputs = {'limit': 2024}

def solve(limit):
    moves = (1, 4)
    if limit < 1:
        return 0
    win = [False] * (limit + 1)
    for n in range(1, limit + 1):
        for m in moves:
            if m <= n and not win[n - m]:
                win[n] = True
                break
    return sum(1 for n in range(1, limit + 1) if not win[n])

solve(2024)

# 调用 solve
result = solve(inputs['limit'])
print(result)