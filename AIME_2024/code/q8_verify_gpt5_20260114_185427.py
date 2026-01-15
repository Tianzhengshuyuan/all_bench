inputs = {'n': 300}

def solve(n):
    S_target = 6_000_000
    # Shortcut when (n/3 - a)(n/3 - b)(n/3 - c) = 0 holds, i.e., 9S - 2n^3 = 0
    if 9 * S_target - 2 * (n ** 3) == 0 and n % 3 == 0:
        return 2 * n + 1

    cnt = 0
    for a in range(n + 1):
        term_a = a * a * (n - a)
        max_b = n - a
        for b in range(max_b + 1):
            c = n - a - b
            S = term_a + b * b * (n - b) + c * c * (n - c)
            if S == S_target:
                cnt += 1
    return cnt

solve(300)

# 调用 solve
result = solve(inputs['n'])
print(result)