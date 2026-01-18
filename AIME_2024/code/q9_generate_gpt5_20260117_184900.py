inputs = {'k': 16}

def solve(k):
    # xy = k^2 / 4; return integer when exact
    if isinstance(k, int) and k % 2 == 0:
        half = k // 2
        return half * half
    return (k * k) / 4

solve(10)

# 调用 solve
result = solve(inputs['k'])
print(result)