from fractions import Fraction
inputs = {'ri_minus_ro': Fraction(99, 28)}

from fractions import Fraction
import math

def solve(ri_minus_ro):
    d = Fraction(ri_minus_ro)
    if d == 0:
        raise ValueError("ri_minus_ro must be nonzero")
    a = Fraction(3, 1)
    R = Fraction(6, 1)

    # Compute sqrt(R^2 + d^2) exactly as a Fraction if possible
    expr = R*R + d*d  # Fraction
    num = expr.numerator
    den = expr.denominator
    sqrt_num = math.isqrt(num)
    sqrt_den = math.isqrt(den)
    if sqrt_num * sqrt_num != num or sqrt_den * sqrt_den != den:
        raise ValueError("The value leads to an irrational radius; cannot represent with Fraction.")
    sqrt_expr = Fraction(sqrt_num, sqrt_den)

    s = a * (R + sqrt_expr) / d
    return s

ri_minus_ro = Fraction(99, 28)
result = solve(ri_minus_ro)

# 调用 solve
result = solve(inputs['ri_minus_ro'])
print(result)