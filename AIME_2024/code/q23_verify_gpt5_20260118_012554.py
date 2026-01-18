inputs = {'a': 20}

def solve(a):
    b = 24
    num = 4 * a * b
    den = b - a
    if den == 0:
        return float('inf')
    if num % den == 0:
        return num // den
    return num / den

solve(20)

# 调用 solve
result = solve(inputs['a'])
print(result)