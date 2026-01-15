inputs = {'inradius': 49}

def solve(inradius):
    R = 13
    r = inradius
    OI2 = R * (R - 2 * r)  # Euler's formula: OI^2 = R(R - 2r)
    AI2 = R * R - OI2      # From AI ⟂ OI: AO^2 = AI^2 + OI^2
    return 3 * AI2         # From geometry: AB * AC = 3 * AI^2

solve(6)

# 调用 solve
result = solve(inputs['inradius'])
print(result)