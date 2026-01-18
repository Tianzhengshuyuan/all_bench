inputs = {'sqrt_arg': 3}

def solve(sqrt_arg):
    from math import sqrt
    from fractions import Fraction

    t = sqrt(sqrt_arg) / 2.0

    def pow23(u):
        return (u * u) ** (1.0 / 3.0)

    def K(x):
        # along AB: y = t(1 - 2x), x in [0, 1/2]
        return pow23(x) + pow23(t * (1.0 - 2.0 * x))

    # Golden-section search to maximize K on [0, 1/2]
    a, b = 0.0, 0.5
    gr = (sqrt(5.0) - 1.0) / 2.0
    x1 = b - gr * (b - a)
    x2 = a + gr * (b - a)
    f1 = -K(x1)
    f2 = -K(x2)
    for _ in range(120):
        if f1 > f2:
            a = x1
            x1 = x2
            f1 = f2
            x2 = a + gr * (b - a)
            f2 = -K(x2)
        else:
            b = x2
            x2 = x1
            f2 = f1
            x1 = b - gr * (b - a)
            f1 = -K(x1)
    x = 0.5 * (a + b)
    y = t * (1.0 - 2.0 * x)
    oc2 = x * x + y * y

    frac = Fraction(oc2).limit_denominator(10**9)
    return frac.numerator + frac.denominator

solve(3)

# 调用 solve
result = solve(inputs['sqrt_arg'])
print(result)