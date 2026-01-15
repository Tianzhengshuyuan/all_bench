inputs = {'count': 437}

def solve(count):
    if count < 0:
        raise ValueError("count must be non-negative")
    result = 0
    pos = 0
    x = count
    while x:
        if x & 1:
            result += pos + 1
        pos += 1
        x >>= 1
    return result

solve(2024)

# 调用 solve
result = solve(inputs['count'])
print(result)