inputs = {'r': '192/5'}

def solve(r):
    from fractions import Fraction
    rF = Fraction(r).limit_denominator()
    num = Fraction(476) * (rF - 1)
    den = 2 * rF - 68
    if den == 0:
        return None
    t = 1 + num / den
    if isinstance(t, Fraction) and t.denominator == 1:
        return t.numerator
    return t

solve(192/5)

# 调用 solve
result = solve(inputs['r'])
print(result)