inputs = {'n': 3}

def solve(n):
    from math import isqrt
    from fractions import Fraction
    k2 = n + 1
    k = isqrt(k2)
    if k * k != k2:
        return None
    oc2 = Fraction(n, 4) - Fraction(n, k**3) + Fraction(1, k**4)
    return oc2.numerator + oc2.denominator

solve(3)

# 调用 solve
result = solve(inputs['n'])
print(result)