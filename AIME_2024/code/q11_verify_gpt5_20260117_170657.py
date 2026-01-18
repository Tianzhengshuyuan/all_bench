inputs = {'a_real': 75}

def solve(a_real):
    import math
    r = 4.0
    A_imag = 117.0
    B_real = 96.0
    B_imag = 144.0
    v_real = r * a_real + (1.0 / r) * B_real
    v_imag = r * A_imag - (1.0 / r) * B_imag
    return math.hypot(v_real, v_imag)

solve(75)

# 调用 solve
result = solve(inputs['a_real'])
print(result)