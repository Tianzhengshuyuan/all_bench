inputs = {'r': 4}

def solve(r):
    r = abs(r)
    A_real, A_imag = 75.0, 117.0
    C_real, C_imag = 96.0, 144.0
    p = A_real * r + C_real / r
    q = C_imag / r - A_imag * r
    val = (p * p + q * q) ** 0.5
    return int(round(val)) if abs(val - round(val)) < 1e-9 else val

solve(4)

# 调用 solve
result = solve(inputs['r'])
print(result)