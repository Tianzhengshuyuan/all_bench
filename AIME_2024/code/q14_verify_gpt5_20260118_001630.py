inputs = {'divisor': 1000}

def solve(divisor):
    if divisor == 0:
        raise ValueError("divisor cannot be zero")
    found = None
    for N in range(9999, 999, -1):
        a = N // 1000
        b = (N // 100) % 10
        c = (N // 10) % 10
        d = N % 10
        digits = (a, b, c, d)
        ok = True
        for place_value, digit in zip((1000, 100, 10, 1), digits):
            M = N + (1 - digit) * place_value
            if M % 7 != 0:
                ok = False
                break
        if ok:
            found = N
            break
    if found is None:
        return None
    Q = found // divisor
    R = found % divisor
    return Q + R

solve(divisor)

# 调用 solve
result = solve(inputs['divisor'])
print(result)