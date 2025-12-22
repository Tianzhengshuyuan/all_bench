inputs = {'n': 3}

def solve(n):
    from math import gcd
    num = 1 + n**3
    den = 64
    g = gcd(num, den)
    p = num // g
    q = den // g
    return p + q

solve(n)

# 调用 solve
result = solve(inputs['n'])
print(result)