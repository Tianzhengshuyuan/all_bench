inputs = {'n': 300}

def solve(n):
    target = 6000000
    # Quick formula case: when target equals 2*n^3/9
    if 2 * (n ** 3) == 9 * target:
        t = n // 3
        return 6 * t + 1
    # Quick impossibility check using upper bound S_max <= n^3/4
    if n ** 3 < 4 * target:
        return 0
    cnt = 0
    for a in range(n + 1):
        na = n - a
        for b in range(na + 1):
            c = na - b
            ab = a * b
            bc = b * c
            ca = c * a
            S = n * (ab + bc + ca) - 3 * a * b * c
            if S == target:
                cnt += 1
    return cnt

solve(300)

# 调用 solve
result = solve(inputs['n'])
print(result)