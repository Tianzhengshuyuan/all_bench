inputs = {'k': 10}

def solve(k):
    res = (k * k) / 4
    try:
        if abs(res - round(res)) < 1e-12:
            return int(round(res))
    except TypeError:
        pass
    return res

solve(10)

# 调用 solve
result = solve(inputs['k'])
print(result)