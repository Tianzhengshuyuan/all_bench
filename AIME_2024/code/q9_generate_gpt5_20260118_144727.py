inputs = {'k': 8}

def solve(k):
    res = (k * k) / 4
    n = round(res)
    if abs(res - n) < 1e-12:
        return int(n)
    return res

# 调用 solve
result = solve(inputs['k'])
print(result)