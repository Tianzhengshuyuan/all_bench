inputs = {'count': 2024}

def solve(count):
    s = 0
    i = 0
    n = count
    while n:
        if n & 1:
            s += i + 1
        n >>= 1
        i += 1
    return s

solve(2024)

# 调用 solve
result = solve(inputs['count'])
print(result)