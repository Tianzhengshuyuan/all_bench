inputs = {'modulus_z': 4}

def solve(modulus_z):
    r = modulus_z
    A = 75 + 96 / (r ** 2)
    B = -117 + 144 / (r ** 2)
    return r * ((A ** 2 + B ** 2) ** 0.5)

# 调用 solve
result = solve(inputs['modulus_z'])
print(result)