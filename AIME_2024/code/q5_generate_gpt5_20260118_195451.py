inputs = {'count_small': 2134}

from fractions import Fraction

def solve(count_small):
    R = 34  # radius of large circles
    C = 8   # count of large circles
    k = count_small

    denom = (k - 1) - R * (C - 1)
    r = Fraction(1, 1) + Fraction((k - 1) * (R - 1), denom)
    return r.numerator + r.denominator

# 调用 solve
result = solve(inputs['count_small'])
print(result)