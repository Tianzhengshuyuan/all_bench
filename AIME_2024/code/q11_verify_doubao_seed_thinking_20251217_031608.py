inputs = {'modulus_z': 4}

def solve(modulus_z):
    r = modulus_z
    k = 75 * r + 96 / r
    m = -117 * r + 144 / r
    return (k ** 2 + m ** 2) ** 0.5

# 调用 solve
result = solve(inputs['modulus_z'])
print(result)