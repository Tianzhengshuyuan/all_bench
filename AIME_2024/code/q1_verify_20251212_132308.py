inputs = {'denominator': 3}

from fractions import Fraction

def solve(denominator):
    s1 = Fraction(1, 2)
    s2 = Fraction(1, denominator)
    s3 = Fraction(1, 4)
    a = -(s2 + s3) / 2
    b = -(s1 + s3) / 2
    c = -(s1 + s2) / 2
    L = abs(4*a + 3*b + 2*c)
    return L.numerator + L.denominator

# 调用 solve
result = solve(inputs['denominator'])
print(result)