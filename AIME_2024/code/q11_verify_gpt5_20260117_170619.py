inputs = {'a_real': 75}

def solve(a_real):
    R = 4.0
    b = 117.0
    c = 96.0
    d = 144.0
    A = complex(a_real, b)
    B = complex(c, d)
    return abs(R * A + B.conjugate() / R)

solve(75)

# 调用 solve
result = solve(inputs['a_real'])
print(result)