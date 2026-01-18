inputs = {'mod': 1000}

def solve(mod):
    def gauss_mul(u, v, m=None):
        a, b = u
        c, d = v
        x = a * c - b * d
        y = a * d + b * c
        if m is not None:
            x %= m
            y %= m
        return (x, y)

    def gauss_pow(base, e, m=None):
        res = (1, 0)
        while e > 0:
            if e & 1:
                res = gauss_mul(res, base, m)
            base = gauss_mul(base, base, m)
            e >>= 1
        return res

    if mod == 0:
        a, b = gauss_pow((1, 1), 13, None)
        return (a - 1) ** 2 + b * b
    else:
        a, b = gauss_pow((1, 1), 13, mod)
        x = (a - 1) % mod
        y = b % mod
        return (x * x + y * y) % mod

# 调用 solve
result = solve(inputs['mod'])
print(result)