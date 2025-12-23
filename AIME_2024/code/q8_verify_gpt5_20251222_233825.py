inputs = {'n': 300}

def solve(n):
    S = 6000000
    if 9 * S == 2 * (n ** 3) and n % 3 == 0:
        return 2 * n + 1
    cnt = 0
    for a in range(n + 1):
        for b in range(n - a + 1):
            c = n - a - b
            ab = a * b
            ac = a * c
            bc = b * c
            if n * (ab + ac + bc) - 3 * ab * c == S:
                cnt += 1
    return cnt

solve(300)

# 调用 solve
result = solve(inputs['n'])
print(result)