inputs = {'hex_side': 80}

def solve(hex_side):
    from fractions import Fraction
    # Known two sides of the big triangle formed by extensions
    a = Fraction(200, 1)
    b = Fraction(240, 1)
    x = Fraction(hex_side, 1)
    denom = Fraction(1, 1) - x * (Fraction(1, a) + Fraction(1, b))
    if denom == 0:
        return float('inf')
    N = x / denom
    return N.numerator // N.denominator if N.denominator == 1 else float(N)

hex_side = 80
solve(hex_side)

# 调用 solve
result = solve(inputs['hex_side'])
print(result)