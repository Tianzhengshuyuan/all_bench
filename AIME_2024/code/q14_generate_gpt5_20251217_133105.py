inputs = {'divisor': 7}

def solve(divisor):
    for N in range(9999, 1000 - 1, -1):
        a = N // 1000
        b = (N // 100) % 10
        c = (N // 10) % 10
        d = N % 10

        candidates = [
            1000 * 1 + 100 * b + 10 * c + d,
            1000 * a + 100 * 1 + 10 * c + d,
            1000 * a + 100 * b + 10 * 1 + d,
            1000 * a + 100 * b + 10 * c + 1,
        ]

        if all(x % divisor == 0 for x in candidates):
            return (N // 1000) + (N % 1000)
    return None

# 调用 solve
result = solve(inputs['divisor'])
print(result)