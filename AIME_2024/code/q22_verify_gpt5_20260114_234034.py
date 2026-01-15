inputs = {'c': 300}

def solve(c):
    a = 200.0
    b = 240.0
    den = 1.0 + c / a + c / b
    x = c / den
    xr = round(x)
    return int(xr) if abs(x - xr) < 1e-9 else x

solve(300)

# 调用 solve
result = solve(inputs['c'])
print(result)