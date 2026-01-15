inputs = {'R': 900}

def solve(R):
    r = 6
    OI2 = R * (R - 2 * r)  # Euler's formula: OI^2 = R^2 - 2Rr = R(R - 2r)
    AI2 = R * R - OI2      # From IA ⟂ OI: AI^2 = AO^2 - OI^2
    return 3 * AI2         # AB * AC = 3 * AI^2

solve(13)

# 调用 solve
result = solve(inputs['R'])
print(result)