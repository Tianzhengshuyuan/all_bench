inputs = {'modulus_z': 4}

def solve(modulus_z):
    r = modulus_z
    a = 75 * r + 96 / r
    b = -117 * r + 144 / r
    return (a ** 2 + b ** 2) ** 0.5

# 调用 solve
result = solve(inputs['modulus_z'])
print(result)