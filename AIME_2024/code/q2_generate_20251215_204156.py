inputs = {'a_x': 99}

from fractions import Fraction

def solve(a_x):
    a = Fraction(a_x)
    numerator = 7 * a**4 - 4 * a**2 + 1
    denominator = 4 * a**2
    oc_squared = numerator / denominator
    return oc_squared.numerator + oc_squared.denominator

# 调用 solve
result = solve(inputs['a_x'])
print(result)