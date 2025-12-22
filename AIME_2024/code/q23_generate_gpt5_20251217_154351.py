inputs = {'denominator_y': 788}

def solve(denominator_y):
    from fractions import Fraction
    d = Fraction(denominator_y, 1)
    # For a valid family of rhombi with perpendicular diagonals crossing the hyperbola,
    # we need d > 20 so that the slope interval (a/b, b/a) is nonempty.
    if d <= 20:
        raise ValueError("denominator_y must be greater than 20.")
    val = Fraction(80) * d / (d - 20)
    return int(val) if val.denominator == 1 else float(val)

# 调用 solve
result = solve(inputs['denominator_y'])
print(result)