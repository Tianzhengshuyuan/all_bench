inputs = {'a': 20}

def solve(a):
    from fractions import Fraction
    b = 24
    A = Fraction(a)
    B = Fraction(b)
    if A == B:
        return float('inf')
    res = 4 * A * B / (B - A)
    return res.numerator if res.denominator == 1 else float(res)

solve(20)

# 调用 solve
result = solve(inputs['a'])
print(result)