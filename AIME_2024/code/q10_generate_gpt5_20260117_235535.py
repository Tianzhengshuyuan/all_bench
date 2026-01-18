inputs = {'count': 1968}

def solve(count):
    if count <= 0:
        return 0
    total = 0
    i = 0
    n = count
    while n:
        if n & 1:
            total += i + 1
        n >>= 1
        i += 1
    return total

solve(2024)

# 调用 solve
result = solve(inputs['count'])
print(result)