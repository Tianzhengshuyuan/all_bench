inputs = {'R': 13}

def solve(R):
    r = 6  # inradius from the problem
    OI2 = R * (R - 2 * r)  # Euler's formula: OI^2 = R(R - 2r)
    AI2 = R * R - OI2      # Right triangle AOI at I: AI^2 = AO^2 - OI^2
    return 3 * AI2         # From geometry: AB * AC = 3 * AI^2

solve(13)

# 调用 solve
result = solve(inputs['R'])
print(result)