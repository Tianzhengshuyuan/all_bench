inputs = {'count': 2024}

def solve(count):
    n = count << 1
    s = 0
    i = 0
    while n:
        if (n & 1) and i >= 1:
            s += i
        n >>= 1
        i += 1
    return s

solve(count)

# 调用 solve
result = solve(inputs['count'])
print(result)