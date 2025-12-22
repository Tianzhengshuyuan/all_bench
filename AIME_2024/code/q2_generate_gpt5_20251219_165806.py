inputs = {'exponent': 2}

def solve(exponent):
    from fractions import Fraction
    # Slope squared of AB: (sqrt(3))^2 = 3
    m2 = Fraction(3, 1)
    # x-coordinate where the root at a=1/2 is double: solve df/da=0 gives x = 1 / (2*(m2+1))
    x = Fraction(1, 2 * (m2 + 1))
    # y = sqrt(3)*(1/2 - x), so y^2 = m2 * (1/2 - x)^2
    dx = Fraction(1, 2) - x
    oc2 = x * x + m2 * (dx * dx)  # OC^2
    if exponent % 2 == 0:
        val = oc2 ** (exponent // 2)
        return val.numerator + val.denominator
    else:
        # For odd exponents, OC^exponent is generally irrational; approximate rationally if needed
        val_float = float(oc2) ** (exponent / 2.0)
        approx = Fraction(val_float).limit_denominator(10**6)
        return approx.numerator + approx.denominator

solve(2)

# 调用 solve
result = solve(inputs['exponent'])
print(result)