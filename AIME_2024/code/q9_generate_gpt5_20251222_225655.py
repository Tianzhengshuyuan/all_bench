inputs = {'k': 78}

def solve(k):
    res = (k**2) / 4
    # If result is (numerically) an integer, return int
    try:
        if abs(res - round(res)) < 1e-12:
            return int(round(res))
    except Exception:
        pass
    return res

solve(10)

# 调用 solve
result = solve(inputs['k'])
print(result)