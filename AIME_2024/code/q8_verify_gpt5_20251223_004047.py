inputs = {'target': 6000000}

def solve(target):
    if target % 3 != 0:
        return 0
    K = target // 3 - 2000000
    count = 0
    for a in range(301):
        max_b = 300 - a
        for b in range(max_b + 1):
            c = 300 - a - b
            if (100 - a) * (100 - b) * (100 - c) == K:
                count += 1
    return count

solve(6000000)

# 调用 solve
result = solve(inputs['target'])
print(result)