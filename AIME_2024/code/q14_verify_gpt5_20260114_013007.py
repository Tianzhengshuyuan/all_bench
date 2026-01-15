inputs = {'divisor': 1000}

def solve(divisor):
    def ok(n):
        a = n // 1000
        b = (n // 100) % 10
        c = (n // 10) % 10
        d = n % 10
        return (
            (1000 + 100 * b + 10 * c + d) % 7 == 0 and
            (1000 * a + 100 + 10 * c + d) % 7 == 0 and
            (1000 * a + 100 * b + 10 + d) % 7 == 0 and
            (1000 * a + 100 * b + 10 * c + 1) % 7 == 0
        )

    N = None
    for n in range(9999, 999, -1):
        if ok(n):
            N = n
            break
    if N is None:
        return None
    q, r = divmod(N, divisor)
    return q + r

solve(1000)

# 调用 solve
result = solve(inputs['divisor'])
print(result)