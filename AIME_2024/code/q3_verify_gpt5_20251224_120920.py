inputs = {'p': '1/115'}

from fractions import Fraction
from math import isqrt

def solve(p):
    pf = Fraction(p).limit_denominator(10**12)
    if pf <= 0:
        return None
    # Closed-form: p = 1 / (3x^2 + x + 1), where x = N - 4
    if pf.numerator == 1:
        D = pf.denominator
        Δ = 12 * D - 11
        s = isqrt(Δ)
        if s * s == Δ and (s - 1) % 6 == 0:
            x = (s - 1) // 6
            if x >= 0 and Fraction(1, 3 * x * x + x + 1) == pf:
                return x + 4
    # Fallback search (in case p is given in a form not exactly a unit fraction after rationalization)
    # Use an estimate for x and search nearby
    try:
        d_guess = int(Fraction(1, 1) / pf)
    except ZeroDivisionError:
        d_guess = 10**6
    x_est = isqrt(max(0, d_guess // 3))
    for x in range(max(0, x_est - 2000), x_est + 2001):
        D = 3 * x * x + x + 1
        if D > 0 and Fraction(1, D) == pf:
            return x + 4
    # Monotone scan until p(N) falls below target
    x = 0
    while True:
        D = 3 * x * x + x + 1
        pN = Fraction(1, D)
        if pN == pf:
            return x + 4
        if pN < pf or x > 10**6:
            break
        x += 1
    return None

solve(1/115)

# 调用 solve
result = solve(inputs['p'])
print(result)