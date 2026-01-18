inputs = {'numerator_real': 96}

def solve(numerator_real):
    r = 4.0
    A = 75.0
    B = 117.0
    D = 144.0
    P = r * A + numerator_real / r
    Q = -r * B + D / r
    res = (P * P + Q * Q) ** 0.5
    return int(res) if res.is_integer() else res

# 调用 solve
result = solve(inputs['numerator_real'])
print(result)