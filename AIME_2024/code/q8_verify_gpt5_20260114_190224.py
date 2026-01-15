inputs = {'n': 300}

def solve(n):
    target = 6_000_000
    if n < 0:
        return 0
    count = 0
    for a in range(n + 1):
        na = n - a
        a_term = a * a * (n - a)
        for b in range(na + 1):
            c = na - b
            x = a_term + b * b * (n - b) + c * c * (n - c)
            if x == target:
                count += 1
    return count

solve(300)

# 调用 solve
result = solve(inputs['n'])
print(result)