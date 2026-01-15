inputs = {'white_chips': 31}

def solve(white_chips):
    import math
    n = math.isqrt(white_chips)
    return (2**n - 2)**2 + 2

solve(25)

# 调用 solve
result = solve(inputs['white_chips'])
print(result)