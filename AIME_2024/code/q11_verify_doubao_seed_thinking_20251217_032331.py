inputs = {'modulus_z': 5}

def solve(modulus_z):
    r = modulus_z
    m = 75 * r + 96 / r
    n = -117 * r + 144 / r
    return int((m ** 2 + n ** 2) ** 0.5)

# 调用 solve
result = solve(inputs['modulus_z'])
print(result)