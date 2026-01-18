inputs = {'count': 2292}

from fractions import Fraction

def solve(count):
    R = 34
    k = 8
    N = count - 1
    K = k - 1
    r = Fraction(R) * Fraction(K - N, R * K - N)
    return r.numerator + r.denominator

solve(2024)

# 调用 solve
result = solve(inputs['count'])
print(result)