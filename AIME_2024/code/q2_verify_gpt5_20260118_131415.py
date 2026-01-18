inputs = {'a': 0.5}

def solve(a):
    from fractions import Fraction
    fa = Fraction(a).limit_denominator()
    oc2 = fa**6 + (1 - fa**2)**3
    oc2 = oc2.limit_denominator()
    return oc2.numerator + oc2.denominator

solve(0.5)

# 调用 solve
result = solve(inputs['a'])
print(result)