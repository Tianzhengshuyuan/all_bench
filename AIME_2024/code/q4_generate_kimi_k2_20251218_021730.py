inputs = {'n': 9552}

def solve(n):
    # Bob wins when n ≡ 0 or 2 (mod 5)
    count = 0
    for i in range(1, n + 1):
        if i % 5 == 0 or i % 5 == 2:
            count += 1
    return count

# 调用 solve
result = solve(inputs['n'])
print(result)