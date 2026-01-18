inputs = {'a': 0.5}

def solve(a):
    from fractions import Fraction
    a = Fraction(a)
    oc2 = a**6 + (Fraction(1) - a**2)**3
    return oc2.numerator + oc2.denominator

solve(0.5)

# 调用 solve
result = solve(inputs['a'])
print(result)