inputs = {'sqrt_arg': 2}

def solve(sqrt_arg):
    from fractions import Fraction
    oc2 = Fraction(1 + 9 * sqrt_arg, 64)
    return oc2.numerator + oc2.denominator

solve(3)

# 调用 solve
result = solve(inputs['sqrt_arg'])
print(result)