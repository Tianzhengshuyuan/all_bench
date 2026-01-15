inputs = {'tri_side1': 235}

def solve(tri_side1):
    from fractions import Fraction
    rKM_KL = Fraction(300, 200)  # KM/KL
    rKM_LM = Fraction(300, 240)  # KM/LM
    denom = rKM_LM + 1 + rKM_KL
    scale = rKM_KL / denom
    x = tri_side1 * scale
    if isinstance(x, Fraction):
        return x.numerator if x.denominator == 1 else float(x)
    return x

solve(200)

# 调用 solve
result = solve(inputs['tri_side1'])
print(result)