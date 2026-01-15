inputs = {'radius': 4}

def solve(radius):
    r = float(abs(radius))
    A = 75 + 117j
    B = 96 + 144j
    if r == 0:
        return float('inf') if (B.real != 0 or B.imag != 0) else 0.0
    return abs(r * A + B.conjugate() / r)

solve(4)

# 调用 solve
result = solve(inputs['radius'])
print(result)