inputs = {'sqrt_arg': 407}

from fractions import Fraction

def solve(sqrt_arg):
    s2 = Fraction(sqrt_arg, 1) if isinstance(sqrt_arg, int) else Fraction(sqrt_arg).limit_denominator()
    x = (s2 - 2) / (2 * (1 + s2))
    t = Fraction(1, 2) - x
    oc2 = x * x + s2 * t * t
    oc2 = Fraction(oc2).limit_denominator()
    return oc2.numerator + oc2.denominator

solve(globals().get('sqrt_arg', 3))

# 调用 solve
result = solve(inputs['sqrt_arg'])
print(result)