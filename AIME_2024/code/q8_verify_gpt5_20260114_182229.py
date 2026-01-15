inputs = {'total': 6000000}

def solve(total):
    S = 300
    if total % 3 != 0:
        return 0
    k = total // 3 - 2_000_000
    count = 0
    for a in range(S + 1):
        for b in range(S - a + 1):
            c = S - a - b
            if (100 - a) * (100 - b) * (100 - c) == k:
                count += 1
    return count

solve(6000000)

# 调用 solve
result = solve(inputs['total'])
print(result)