inputs = {'n': 300}

def solve(n):
    K = 6_000_000
    # Special fast path when (n/3 - a)(n/3 - b)(n/3 - c) = 0 holds, i.e., 9K == 2 n^3
    if n % 3 == 0 and 9 * K == 2 * n ** 3:
        return 2 * n + 1
    count = 0
    for a in range(n + 1):
        max_b = n - a
        for b in range(max_b + 1):
            c = n - a - b
            S = a * a * (n - a) + b * b * (n - b) + c * c * (n - c)
            if S == K:
                count += 1
    return count

solve(300)

# 调用 solve
result = solve(inputs['n'])
print(result)