inputs = {'count': 2024}

def solve(count):
    n = int(count)
    if n < 0:
        raise ValueError("count must be nonnegative")
    res = 0
    pos = 1
    while n:
        if n & 1:
            res += pos
        n >>= 1
        pos += 1
    return res

if 'count' in globals():
    solve(count)

# 调用 solve
result = solve(inputs['count'])
print(result)