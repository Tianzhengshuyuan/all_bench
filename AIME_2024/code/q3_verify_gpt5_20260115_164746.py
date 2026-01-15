from fractions import Fraction
inputs = {'p_grand_given_prize': Fraction(1, 115)}

from fractions import Fraction
import math

def solve(p_grand_given_prize):
    p = p_grand_given_prize if isinstance(p_grand_given_prize, Fraction) else Fraction(p_grand_given_prize)
    if p == 0:
        return None
    T = Fraction(1, 1) / p
    if T.denominator != 1:
        return None
    t = T.numerator
    # Solve 3N^2 - 23N + 45 = t
    D = 23*23 - 12*(45 - t)
    if D < 0:
        return None
    r = math.isqrt(D)
    if r * r != D:
        return None
    candidates = []
    for sign in (1, -1):
        num = 23 + sign * r
        if num % 6 == 0:
            N = num // 6
            if N >= 4:
                if 3 * N * N - 23 * N + 45 == t:
                    candidates.append(N)
    if not candidates:
        return None
    return min(candidates)

result = solve(Fraction(1, 115))

# 调用 solve
result = solve(inputs['p_grand_given_prize'])
print(result)