inputs = {'a': 75}

def solve(a):
    r = 4.0
    c = complex(a, 117.0)
    d = complex(96.0, 144.0)
    K = r * c + d.conjugate() / r
    return abs(K)

solve(75)

# 调用 solve
result = solve(inputs['a'])
print(result)