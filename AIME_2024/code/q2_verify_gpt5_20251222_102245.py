inputs = {'n': 3}

def solve(n):
    from math import gcd
    p = n + 4
    q = 4 * (n + 1)
    g = gcd(p, q)
    p //= g
    q //= g
    return p + q

solve(3)

# 调用 solve
result = solve(inputs['n'])
print(result)