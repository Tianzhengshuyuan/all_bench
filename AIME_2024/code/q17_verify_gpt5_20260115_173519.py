from fractions import Fraction
inputs = {'r2': Fraction(657, 64)}

from fractions import Fraction
import math

def solve(r2):
    r2 = Fraction(r2)

    p = r2.numerator
    q = r2.denominator

    # Polynomial in t = a^2: 2 t^3 - 4 r2 t^2 + 529 = 0
    # Clear denominators: (2q) t^3 + (-4p) t^2 + (529q) = 0
    A = 2 * q
    B = -4 * p
    D = 529 * q

    def divisors(n):
        n = abs(n)
        divs = set()
        lim = int(math.isqrt(n))
        for i in range(1, lim + 1):
            if n % i == 0:
                divs.add(i)
                divs.add(n // i)
        return sorted(divs)

    # Generate rational root candidates for t using Rational Root Theorem
    cand = set()
    for num in divisors(D):
        for den in divisors(A):
            cand.add(Fraction(num, den))
            cand.add(Fraction(-num, den))

    # Evaluate polynomial exactly with Fractions
    roots = []
    for t in cand:
        val = Fraction(A, 1) * t**3 + Fraction(B, 1) * t**2 + Fraction(D, 1)
        if val == 0:
            roots.append(t)

    proots = [t for t in roots if t > 0]

    def rational_sqrt(fr):
        num = fr.numerator
        den = fr.denominator
        sn = int(math.isqrt(num))
        sd = int(math.isqrt(den))
        if sn * sn == num and sd * sd == den:
            return Fraction(sn, sd)
        return None

    # For each positive rational root t, check if sqrt(t) is rational.
    # If so, compute S = 2 * (t + 46 / sqrt(t)).
    for t in proots:
        s = rational_sqrt(t)
        if s is not None:
            S = 2 * (t + Fraction(46, 1) / s)
            return S.numerator if S.denominator == 1 else S

    raise ValueError("No suitable rational solution found for the given r^2.")

solve(Fraction(657, 64))

# 调用 solve
result = solve(inputs['r2'])
print(result)