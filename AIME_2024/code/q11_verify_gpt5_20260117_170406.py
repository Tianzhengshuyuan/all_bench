inputs = {'a_real': 75}

def solve(a_real):
    import math
    R = 4.0
    b = 117.0
    c = 96.0
    d = 144.0
    real_part = R * a_real + c / R
    imag_part = R * b - d / R
    return math.hypot(real_part, imag_part)

solve(75)

# 调用 solve
result = solve(inputs['a_real'])
print(result)