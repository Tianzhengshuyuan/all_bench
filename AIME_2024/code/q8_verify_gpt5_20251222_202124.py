inputs = {'n': 300}

def solve(n):
    target = 6000000
    # Special fast path when S equals 6*(n/3)^3
    if n % 3 == 0:
        k = n // 3
        if 6 * (k ** 3) == target:
            # Count ordered triples with a+b+c=n and at least one equals k
            # Inclusion-exclusion gives 2*n + 1
            return 2 * n + 1
    # General case: brute-force enumeration
    cnt = 0
    for a in range(n + 1):
        a_term = a * a * (n - a)
        na = n - a
        for b in range(na + 1):
            c = na - b
            S = a_term + b * b * (n - b) + c * c * (n - c)
            if S == target:
                cnt += 1
    return cnt

solve(300)

# 调用 solve
result = solve(inputs['n'])
print(result)