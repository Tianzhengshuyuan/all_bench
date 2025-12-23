inputs = {'r': 4}

def solve(r):
    r = abs(r)
    A_real, A_imag = 75.0, 117.0
    B_real, B_imag = 96.0, 144.0
    return ((A_real * r + B_real / r) ** 2 + (B_imag / r - A_imag * r) ** 2) ** 0.5

solve(r)

# 调用 solve
result = solve(inputs['r'])
print(result)