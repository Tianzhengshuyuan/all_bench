inputs = {'power': 2}

def solve(power):
    from fractions import Fraction
    from math import gcd

    # Solve for x such that a=1/2 is a double root: 16x^2 - 10x + 1 = 0
    # Roots: (10 ± 6)/32 = 1/2, 1/8. Choose interior point distinct from A and B -> x = 1/8
    roots = [Fraction(10 - 6, 32), Fraction(10 + 6, 32)]
    x = None
    for r in roots:
        if Fraction(0, 1) < r < Fraction(1, 2):
            x = r
            break

    # Compute OC^2 = x^2 + 3(1/2 - x)^2
    half = Fraction(1, 2)
    r2 = x * x + 3 * (half - x) * (half - x)  # should be 7/16

    # Compute p+q where OC^power = p/q in lowest terms (only defined for even integer power)
    if power % 2 == 0:
        k = abs(power) // 2
        num = pow(r2.numerator, k)
        den = pow(r2.denominator, k)
        if power < 0:
            num, den = den, num
        g = gcd(num, den)
        num //= g
        den //= g
        return num + den
    else:
        # For odd power, OC^power is irrational (since OC^2 is 7/16), no p/q representation.
        # Raise to signal unsupported case per problem statement generalization.
        raise ValueError("OC^power is irrational for odd power; no p/q representation.")

solve(power)

# 调用 solve
result = solve(inputs['power'])
print(result)