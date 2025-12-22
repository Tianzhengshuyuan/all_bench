inputs = {'modulus_z': 5}

def solve(modulus_z):
    r = modulus_z
    r_sq = r ** 2
    A = 75 + 96 / r_sq
    B = -117 + 144 / r_sq
    C = (A ** 2 + B ** 2) ** 0.5
    return r * C

# 调用 solve
result = solve(inputs['modulus_z'])
print(result)