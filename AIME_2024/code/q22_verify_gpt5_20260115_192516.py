inputs = {'hexagon_side': 80}

def solve(hexagon_side):
    from fractions import Fraction
    # Known sides of the large triangle
    A = Fraction(200, 1)
    B = Fraction(240, 1)
    # Convert input to Fraction for exact arithmetic
    try:
        x = Fraction(hexagon_side)
    except Exception:
        x = Fraction(str(hexagon_side))
    # Derived from similarity and collinearity:
    # N = x / (1 - x*(1/A + 1/B)) = x*A*B / (A*B - x*(A+B))
    numerator = x * A * B
    denominator = A * B - x * (A + B)
    if denominator == 0:
        return float('inf')
    N = numerator / denominator
    return int(N) if isinstance(N, Fraction) and N.denominator == 1 else float(N)

hexagon_side = 80
solve(hexagon_side)

# 调用 solve
result = solve(inputs['hexagon_side'])
print(result)