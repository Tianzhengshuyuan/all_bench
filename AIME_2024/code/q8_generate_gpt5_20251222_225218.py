inputs = {'n': 336}

def solve(n):
    target = 6000000
    count = 0
    for a in range(n + 1):
        for b in range(n - a + 1):
            c = n - a - b
            t = a * a * (n - a) + b * b * (n - b) + c * c * (n - c)
            if t == target:
                count += 1
    return count

solve(300)

# 调用 solve
result = solve(inputs['n'])
print(result)