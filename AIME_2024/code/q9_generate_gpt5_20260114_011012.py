inputs = {'n': 228}

def solve(n):
    # From log properties: 4xy = n^2 => xy = n^2 / 4
    if isinstance(n, int):
        q, r = divmod(n * n, 4)
        return q if r == 0 else (n * n) / 4
    return (n * n) / 4

solve(10)

# 调用 solve
result = solve(inputs['n'])
print(result)