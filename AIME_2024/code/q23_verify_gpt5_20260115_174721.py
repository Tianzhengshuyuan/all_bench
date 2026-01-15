inputs = {'bd2_lower_bound': 480}

def solve(bd2_lower_bound):
    from fractions import Fraction
    B = Fraction(24, 1)
    # Use Fraction to avoid precision issues
    try:
        L = Fraction(bd2_lower_bound)
    except TypeError:
        L = Fraction(str(bd2_lower_bound))
    N = (B * L) / (L + 4 * B)
    return N.numerator if N.denominator == 1 else float(N)

solve(480)

# 调用 solve
result = solve(inputs['bd2_lower_bound'])
print(result)