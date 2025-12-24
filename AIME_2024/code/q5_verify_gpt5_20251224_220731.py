inputs = {'inradius_numerator': 192}

def solve(inradius_numerator):
    from fractions import Fraction
    N = inradius_numerator  # inradius r = N/5
    # Derived relation: k = 1 + 238*(N - 5)/(N - 170)
    denom = N - 170
    if denom == 0:
        return None
    k = Fraction(1, 1) + Fraction(238 * (N - 5), denom)
    return k.numerator if k.denominator == 1 else k

solve(192)

# 调用 solve
result = solve(inputs['inradius_numerator'])
print(result)