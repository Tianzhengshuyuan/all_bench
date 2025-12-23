inputs = {'count': 2024}

def solve(count):
    x = count
    s = 0
    pos = 0
    while x:
        if x & 1:
            s += pos + 1
        x >>= 1
        pos += 1
    return s

solve(count)

# 调用 solve
result = solve(inputs['count'])
print(result)