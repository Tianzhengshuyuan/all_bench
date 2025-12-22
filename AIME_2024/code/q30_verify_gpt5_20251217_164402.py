inputs = {'modulus': 450}

def solve(modulus):
    # Compute (1+i)^13 using Gaussian integer exponentiation
    def pow_gauss(a, b, n):
        ra, rb = 1, 0  # (1 + 0i)
        while n:
            if n & 1:
                ra, rb = ra * a - rb * b, ra * b + rb * a
            a, b = a * a - b * b, 2 * a * b
            n >>= 1
        return ra, rb

    x, y = pow_gauss(1, 1, 13)  # (1+i)^13 = x + yi
    product_value = (x - 1) * (x - 1) + y * y  # |(1+i)^13 - 1|^2
    return product_value % modulus

# 调用 solve
result = solve(inputs['modulus'])
print(result)