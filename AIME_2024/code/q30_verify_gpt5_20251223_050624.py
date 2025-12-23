inputs = {'modulus': 1000}

def solve(modulus):
    # Gaussian integer multiplication
    def mul(z1, z2):
        a, b = z1
        c, d = z2
        return (a*c - b*d, a*d + b*c)

    # Exponentiation by squaring for Gaussian integers
    def pow_gauss(z, n):
        res = (1, 0)  # 1 + 0i
        base = z
        e = n
        while e > 0:
            if e & 1:
                res = mul(res, base)
            base = mul(base, base)
            e >>= 1
        return res

    # Compute z = (1+i)^13 - 1
    z = pow_gauss((1, 1), 13)
    z_minus_one = (z[0] - 1, z[1])

    # Norm: (a + bi)(a - bi) = a^2 + b^2 = desired product
    value = z_minus_one[0] * z_minus_one[0] + z_minus_one[1] * z_minus_one[1]
    return value % modulus

modulus = 1000
solve(modulus)

# 调用 solve
result = solve(inputs['modulus'])
print(result)