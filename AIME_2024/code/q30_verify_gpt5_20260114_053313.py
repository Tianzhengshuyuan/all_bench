inputs = {'modulus': 1000}

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

    # A = (1 + i)^13 as Gaussian integer
    A_re, A_im = gpow((1, 1), 13)

    # Product equals ( (1+i)^13 - 1 ) ( (1-i)^13 - 1 )
    # = ((1+i)^13 (1-i)^13) - ((1+i)^13 + (1-i)^13) + 1
    # = 2^13 - 2*Re((1+i)^13) + 1
    AB = 2 ** 13
    S = 2 * A_re
    val = AB - S + 1
    return val % modulus

solve(modulus)

# 调用 solve
result = solve(inputs['modulus'])
print(result)