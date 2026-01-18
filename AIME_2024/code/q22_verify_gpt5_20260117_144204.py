inputs = {'c': 300}

def solve(c):
    from fractions import Fraction
    a = Fraction(200, 1)
    b = Fraction(240, 1)
    c_frac = Fraction(c, 1)
    denom = (c_frac / b) + Fraction(1, 1) + (c_frac / a)
    x = c_frac / denom
    return x.numerator if x.denominator == 1 else float(x)

solve(300)

# 调用 solve
result = solve(inputs['c'])
print(result)