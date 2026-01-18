inputs = {'divisor': 1000}

def solve(divisor):
    for N in range(9999, 999, -1):
        s = str(N)
        ok = True
        for i in range(4):
            if int(s[:i] + '1' + s[i+1:]) % 7 != 0:
                ok = False
                break
        if ok:
            q, r = divmod(N, divisor)
            return q + r
    return None

solve(1000)

# 调用 solve
result = solve(inputs['divisor'])
print(result)