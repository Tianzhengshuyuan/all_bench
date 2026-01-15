inputs = {'BC_length': 9}

def solve(BC_length):
    from fractions import Fraction
    from math import isqrt, sqrt

    AB = 5
    AC = 10
    c = Fraction(BC_length, 1)

    # Using Apollonius: 4*AM^2 = 2(AB^2 + AC^2) - c^2
    X = Fraction(2 * (AB * AB + AC * AC), 1) - c * c  # X = 250 - c^2 for AB=5, AC=10

    if X <= 0:
        return None

    num, den = X.numerator, X.denominator
    rnum, rden = isqrt(num), isqrt(den)

    if rnum * rnum == num and rden * rden == den:
        # sqrt(X) is rational
        sqrtX = Fraction(rnum, rden)
        AP = Fraction(2 * AB * AC, 1) / sqrtX  # AP = 2AB*AC / sqrt(X)
        if AP < 0:
            AP = -AP
        return AP.numerator + AP.denominator
    else:
        # sqrt(X) is irrational; return numeric AP (m+n is undefined in this case)
        AP_float = (2 * AB * AC) / sqrt(num / den)
        return AP_float

solve(9)

# 调用 solve
result = solve(inputs['BC_length'])
print(result)