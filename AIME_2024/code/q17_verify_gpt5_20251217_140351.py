inputs = {'volume': 23}

from math import acos, cos, sqrt, isclose, pi
from fractions import Fraction
from itertools import chain

def solve(volume):
    V = Fraction(volume)
    S = 54  # fixed surface area in the problem
    A = S // 2  # ab + bc + ca = 27

    # We consider extremal boxes with two equal edges: let b=c=x, a=y.
    # Constraints: x^2 + 2xy = A and x^2 y = V
    # Eliminating y gives: 2V/x + x^2 = A  =>  x^3 - A x + 2V = 0
    # Solve cubic for positive real roots x, then y = V/x^2, and diagonal^2 = a^2 + b^2 + c^2 = y^2 + 2x^2.
    # r^2 = diagonal^2 / 4. We take the maximal r^2 over positive roots.

    # Cubic: x^3 + p x + q = 0 with p = -A, q = 2V
    p = -Fraction(A)
    q = 2 * V

    # Collect positive real roots (integers first via Rational Root Theorem; the polynomial is monic)
    int_roots = set()
    const_term = q  # equals 2V as Fraction
    # Candidate integer roots divide 2V's numerator when over denominator 1.
    # Ensure integer candidates: consider divisors of 2*volume (since q is integer when volume is integer)
    if const_term.denominator == 1:
        C = abs(const_term.numerator)
        # enumerate divisors
        divs = set()
        i = 1
        while i * i <= C:
            if C % i == 0:
                divs.add(i)
                divs.add(C // i)
            i += 1
        for d in sorted(divs):
            for sgn in (1, -1):
                x = sgn * d
                # Evaluate x^3 + p x + q exactly
                val = x**3 + p * x + q
                if val == 0:
                    if x > 0:
                        int_roots.add(x)

    # Numeric roots via depressed cubic solution
    roots = set(float(r) for r in int_roots)  # start with integer roots as floats

    # Convert p, q to floats for numeric solving
    p_f = float(p)
    q_f = float(q)
    D = (q_f / 2.0) ** 2 + (p_f / 3.0) ** 3  # Cardano's discriminant

    def cbrt(x):
        return (abs(x) ** (1.0 / 3.0)) * (1 if x >= 0 else -1)

    numeric_roots = []
    if D >= 0:
        # One real root
        u = cbrt(-q_f / 2.0 + sqrt(D))
        v = cbrt(-q_f / 2.0 - sqrt(D))
        numeric_roots = [u + v]
    else:
        # Three real roots via trigonometric form
        r = 2.0 * sqrt(-p_f / 3.0)
        # Avoid domain issues due to tiny numerical noise
        arg = (-q_f / 2.0) / sqrt((-p_f / 3.0) ** 3)
        arg = max(-1.0, min(1.0, arg))
        theta = acos(arg)
        numeric_roots = [r * cos((theta + 2.0 * pi * k) / 3.0) for k in range(3)]

    # Merge numeric positive roots with deduplication
    for x in numeric_roots:
        if x > 1e-12:
            # Deduplicate against existing
            if not any(isclose(x, r, rel_tol=1e-12, abs_tol=1e-12) for r in roots):
                roots.add(x)

    # Evaluate r^2 for each positive root; prefer exact Fraction when root is integer
    best_r2_frac = None
    best_r2_float = None
    for xf in roots:
        # Check if this root is one of our exact integer roots
        nearest_int = int(round(xf))
        if any(abs(nearest_int - xi) < 1e-12 for xi in int_roots) and isclose(xf, nearest_int, rel_tol=0, abs_tol=1e-12):
            x_int = nearest_int
            x2 = x_int * x_int
            y = Fraction(V, x2)
            d2 = y * y + 2 * x2
            r2 = d2 / 4
            if best_r2_frac is None or r2 > best_r2_frac:
                best_r2_frac = r2
                best_r2_float = float(r2)
        else:
            # Numeric path
            x = xf
            y = float(V) / (x * x)
            d2 = y * y + 2.0 * x * x
            r2 = d2 / 4.0
            if best_r2_float is None or r2 > best_r2_float:
                best_r2_float = r2

    # Decide final r^2 as Fraction
    if best_r2_frac is not None:
        r2_frac = best_r2_frac
    else:
        # Fallback: approximate as Fraction
        r2_frac = Fraction(best_r2_float).limit_denominator(10**9)

    # Return p + q where r^2 = p/q in lowest terms
    r2_frac = r2_frac.limit_denominator()
    return r2_frac.numerator + r2_frac.denominator

# Example:
# print(solve(23))  # Expected 721

# 调用 solve
result = solve(inputs['volume'])
print(result)