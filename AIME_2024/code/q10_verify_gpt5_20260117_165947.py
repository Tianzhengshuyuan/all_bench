inputs = {'count': 2024}

def solve(count):
    n = count
    total = 0
    pos = 0
    while n > 0:
        if n & 1:
            total += pos + 1
        pos += 1
        n >>= 1
    return total

solve(count)

# 调用 solve
result = solve(inputs['count'])
print(result)