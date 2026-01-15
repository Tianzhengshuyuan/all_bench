inputs = {'path_count': 294}

def solve(path_count):
    P = int(path_count)
    if P < 0:
        return None
    x = 1  # x = N - 1
    while True:
        val = x * x * (x - 1)
        if val == P:
            return x + 1
        if val > P:
            return None
        x += 1

solve(path_count)

# 调用 solve
result = solve(inputs['path_count'])
print(result)