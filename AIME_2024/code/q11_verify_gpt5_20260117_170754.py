inputs = {'a_real': 75}

def solve(a_real):
    import math
    r = 4.0
    c1, c2 = a_real, 117.0
    d1, d2 = 96.0, 144.0
    u = c1 + d1 / (r * r)
    v = -c2 + d2 / (r * r)
    ans = r * math.hypot(u, v)
    return int(round(ans)) if abs(ans - round(ans)) < 1e-9 else ans

solve(75)

# 调用 solve
result = solve(inputs['a_real'])
print(result)