inputs = {'radicand': 3}

def solve(radicand):
    from math import gcd
    num = 9 * radicand + 1
    den = 64
    g = gcd(num, den)
    p = num // g
    q = den // g
    return p + q

solve(3)

# 调用 solve
result = solve(inputs['radicand'])
print(result)