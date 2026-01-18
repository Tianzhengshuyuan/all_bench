inputs = {'power': 6}

def solve(power):
    from fractions import Fraction
    # AB is a unit segment with intercepts a=1/2 (x-axis) and b such that a^2 + b^2 = 1
    a2 = Fraction(1, 4)
    b2 = Fraction(1, 1) - a2  # = 3/4
    # For the astroid envelope, C = (a^3, b^3), hence OC^2 = a^6 + b^6 = (a^2)^3 + (b^2)^3
    t = a2**3 + b2**3  # = 7/16
    if power % 2 != 0:
        raise ValueError("power must be even for OC^power to be rational")
    k = power // 2
    base = t
    if k >= 0:
        frac = base ** k
    else:
        frac = Fraction(1, 1) / (base ** (-k))
    return frac.numerator + frac.denominator

# 调用 solve
result = solve(inputs['power'])
print(result)