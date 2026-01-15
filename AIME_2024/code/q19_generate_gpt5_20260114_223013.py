inputs = {'r': 67}

def solve(r):
    R = 13
    OI2 = R * (R - 2 * r)  # Euler's formula: OI^2 = R(R - 2r)
    AI2 = R * R - OI2      # Right triangle AOI: AI^2 = AO^2 - OI^2
    return 3 * AI2         # From geometry: AB * AC = 3 * AI^2

solve(6)

# 调用 solve
result = solve(inputs['r'])
print(result)