inputs = {'numerator_real': 96}

def solve(numerator_real):
    import math
    A = 4 * (75 + 114j)
    B = 0.25 * (numerator_real + 144j)
    P = (A + B).real
    Q = (B - A).imag
    val = math.hypot(P, Q)
    if abs(val - round(val)) < 1e-9:
        return int(round(val))
    return val

# 调用 solve
result = solve(inputs['numerator_real'])
print(result)