inputs = {'a_real': 75}

def solve(a_real):
    import math
    R = 4.0
    b = 117.0
    c = 96.0
    d = 144.0
    x = R * a_real + c / R
    y = R * b - d / R
    return math.hypot(x, y)

solve(75)

# 调用 solve
result = solve(inputs['a_real'])
print(result)