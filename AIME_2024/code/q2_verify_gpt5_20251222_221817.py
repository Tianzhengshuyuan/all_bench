inputs = {'n': 3}

def solve(n):
    import math
    p = 1 + n**3
    q = 64
    g = math.gcd(p, q)
    p //= g
    q //= g
    return p + q

solve(n)

# 调用 solve
result = solve(inputs['n'])
print(result)