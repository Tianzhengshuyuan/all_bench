inputs = {'a2': 20}

def solve(a2):
    b2 = 24
    num = 4 * a2 * b2
    den = b2 - a2
    if isinstance(a2, int) and den != 0 and num % den == 0:
        return num // den
    return num / den

solve(20)

# 调用 solve
result = solve(inputs['a2'])
print(result)