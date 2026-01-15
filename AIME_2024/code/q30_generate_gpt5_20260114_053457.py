inputs = {'modulus': 617}

def solve(modulus):
    def mul(z1, z2):
        a, b = z1
        c, d = z2
        return (a * c - b * d, a * d + b * c)

    def gpow(base, exp):
        res = (1, 0)
        while exp > 0:
            if exp & 1:
                res = mul(res, base)
            base = mul(base, base)
            exp >>= 1
        return res

    A_re, _ = gpow((1, 1), 13)
    val = (1 << 13) - 2 * A_re + 1
    return val % modulus

solve(1000)

# 调用 solve
result = solve(inputs['modulus'])
print(result)