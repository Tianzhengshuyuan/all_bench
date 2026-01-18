inputs = {'b2': 24}

def solve(b2):
    a2 = 20
    num = 4 * a2 * b2 * (a2 + b2)
    den = b2 * b2 - a2 * a2
    if den == 0:
        return float('inf')
    if num % den == 0:
        return num // den
    return num / den

# 调用 solve
result = solve(inputs['b2'])
print(result)