inputs = {'m': 3}

def solve(m):
    from math import gcd
    # From the derivation, x_C = 1/8 and y_C = -sqrt(m)*x_C + sqrt(m)/2 = 3*sqrt(m)/8
    # Hence OC^2 = x_C^2 + y_C^2 = 1/64 + 9m/64 = (1 + 9m)/64
    p = 9 * m + 1
    q = 64
    g = gcd(p, q)
    p //= g
    q //= g
    return p + q

solve(3)

# 调用 solve
result = solve(inputs['m'])
print(result)