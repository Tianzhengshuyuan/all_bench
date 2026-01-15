inputs = {'radius': 4}

def solve(radius):
    r = float(abs(radius))
    A = 75 + 117j
    B = 96 + 144j
    if r == 0.0:
        return 0.0 if (B.real == 0.0 and B.imag == 0.0) else float('inf')
    val = abs(r * A + B.conjugate() / r)
    iv = round(val)
    return int(iv) if abs(val - iv) < 1e-12 else val

solve(4)

# 调用 solve
result = solve(inputs['radius'])
print(result)