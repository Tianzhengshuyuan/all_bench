inputs = {'divisor': 368}

def solve(divisor):
    for n in range(9999, 999, -1):
        ok = True
        for p in (1, 10, 100, 1000):
            replaced = n - ((n // p) % 10) * p + p
            if replaced % 7 != 0:
                ok = False
                break
        if ok:
            q, r = divmod(n, divisor)
            return q + r
    return None

solve(1000)

# 调用 solve
result = solve(inputs['divisor'])
print(result)