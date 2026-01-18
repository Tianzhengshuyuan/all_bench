inputs = {'a_real': 75}

def solve(a_real):
    R = 4.0
    coef1 = complex(a_real, 117.0)
    coef2 = complex(96.0, 144.0)
    A = R * coef1
    B = (1.0 / R) * coef2
    C = A + B.conjugate()
    return abs(C)

solve(75)

# 调用 solve
result = solve(inputs['a_real'])
print(result)