inputs = {'count': 2074}

def solve(count):
    n = int(count)
    if n <= 0:
        return 0
    total = 0
    i = 0
    while n:
        if n & 1:
            total += i + 1
        i += 1
        n >>= 1
    return total

# 调用 solve
result = solve(inputs['count'])
print(result)