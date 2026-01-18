inputs = {'k': 3}

from fractions import Fraction

def solve(k):
    k = Fraction(k)
    value = (k*k - k + 1) / ((k + 1) * (k + 1))
    num = value.numerator
    den = value.denominator
    if den < 0:
        num, den = -num, -den
    return num + den

solve(k)

# 调用 solve
result = solve(inputs['k'])
print(result)