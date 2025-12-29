inputs = {'path_count': 294}

def solve(path_count):
    if path_count < 0:
        return None
    n = 1
    while True:
        count = (n - 1) * (n - 1) * (n - 2) if n >= 2 else 0
        if count == path_count:
            return n
        if n >= 2 and count > path_count:
            return None
        n += 1

solve(294)

# 调用 solve
result = solve(inputs['path_count'])
print(result)