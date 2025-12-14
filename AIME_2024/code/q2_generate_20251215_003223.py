inputs = {'n': 3}

from fractions import Fraction
import math

def solve(n: int) -> int:
    k2 = n + 1
    k = math.isqrt(k2)
    if k * k != k2:
        # For general n, the special point exists uniquely (as in the problem) only when 1+n is a perfect square,
        # which ensures AB is in the family and the limit yields a rational value.
        # Since the original problem has n=3 (k=2), we handle that (and similar) cases.
        raise ValueError("This setup yields a rational OC^2 only when 1+n is a perfect square.")
    # OC^2 = 1/k^6 + n * (1/k^6 - 1/k^3 + 1/4)
    oc2 = Fraction(1, k**6) + n * (Fraction(1, k**6) - Fraction(1, k**3) + Fraction(1, 4))
    oc2 = oc2.limit_denominator()
    return oc2.numerator + oc2.denominator

# 调用 solve
result = solve(inputs['n'])
print(result)