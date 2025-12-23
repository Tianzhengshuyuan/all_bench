inputs = {'surface_area': 54}

from fractions import Fraction
import math

def solve(surface_area):
    V = 23  # fixed by the problem
    s = Fraction(surface_area, 1)

    # Cubic for x=b=c: 2x^3 - s x + 4V = 0
    a, b, c, d = 2, 0, -s, Fraction(4*V, 1)

    def divisors(n):
        n = abs(n)
        divs = set()
        for i in range(1, int(n**0.5) + 1):
            if n % i == 0:
                divs.add(i)
                divs.add(n // i)
        return sorted(divs)

    # Find rational roots using Rational Root Theorem (for integer coefficients)
    def rational_roots_cubic(a, b, c, d):
        # a, b, c, d are integers or Fractions; scale to integers
        # We assume a and d are integers already; c may be Fraction if s not integer
        # Multiply equation by L to clear denominators (here s is integer in our use-case)
        if isinstance(a, Fraction): a = a.numerator // a.denominator
        if isinstance(b, Fraction): b = b.numerator // b.denominator
        if isinstance(c, Fraction): 
            if c.denominator != 1:
                L = c.denominator
                a *= L
                b *= L
                c = c.numerator
                d *= L
            else:
                c = c.numerator
        if isinstance(d, Fraction): d = d.numerator // d.denominator

        roots = []
        qa = abs(a)
        q_divs = divisors(qa if qa != 0 else 1)
        p_divs = divisors(abs(d))
        for p in p_divs:
            for q in q_divs:
                for sign in (1, -1):
                    r = Fraction(sign * p, q)
                    val = a*r**3 + b*r**2 + c*r + d
                    if val == 0:
                        roots.append(r)
        # Remove duplicates
        roots = list(dict.fromkeys(roots))
        return roots

    # Solve monic cubic x^3 + p x + q = 0 for real roots
    def cubic_real_roots_monic(p, q):
        P = float(p)
        Q = float(q)
        Δ = (Q/2.0)**2 + (P/3.0)**3
        roots = []
        if Δ > 0:
            A = -Q/2.0 + math.sqrt(Δ)
            B = -Q/2.0 - math.sqrt(Δ)
            def cbrt(z):
                return math.copysign(abs(z)**(1.0/3.0), z)
            x = cbrt(A) + cbrt(B)
            roots = [x]
        elif abs(Δ) <= 1e-15:
            # multiple roots
            if abs(Q/2.0) < 1e-15:
                roots = [0.0, 0.0, 0.0]
            else:
                def cbrt(z):
                    return math.copysign(abs(z)**(1.0/3.0), z)
                u = cbrt(-Q/2.0)
                roots = [2*u, -u, -u]
        else:
            # three real roots
            r = 2.0*math.sqrt(-P/3.0)
            phi = math.acos((3.0*Q/(2.0*P))*math.sqrt(-3.0/P))
            roots = [r*math.cos((phi + 2.0*math.pi*k)/3.0) for k in range(3)]
        return roots

    # Find rational roots
    rat_roots = rational_roots_cubic(a, b, c, d)
    rat_positive = [r for r in rat_roots if r > 0]

    # Find all real roots numerically for comparison
    p_m = -s / 2  # since divide by 2: x^3 + p x + q = 0
    q_m = Fraction(2*V, 1)
    real_roots = cubic_real_roots_monic(float(p_m), float(q_m))
    pos_real_roots = [x for x in real_roots if x > 0]

    # Compute D = y^2 + 2x^2 for each candidate
    def D_from_x_fraction(x_frac):
        x2 = x_frac * x_frac
        y = Fraction(V, 1) / x2
        return y*y + 2*x2  # Fraction

    def D_from_x_float(x_float):
        y = V / (x_float**2)
        return y*y + 2*(x_float**2)  # float

    best_D = -1.0
    best_x_is_rational = False
    best_x_fraction = None

    # Check rational candidates exactly
    for xr in rat_positive:
        D_val = D_from_x_fraction(xr)
        D_float = float(D_val)
        if D_float > best_D:
            best_D = D_float
            best_x_is_rational = True
            best_x_fraction = xr

    # Check numeric roots too
    for xf in pos_real_roots:
        Df = D_from_x_float(xf)
        if Df > best_D:
            best_D = Df
            best_x_is_rational = False
            best_x_fraction = None

    # Compute r^2 and return p+q
    if best_x_is_rational and best_x_fraction is not None:
        D_exact = D_from_x_fraction(best_x_fraction)
        r2 = D_exact / 4
        r2 = r2.limit_denominator()
        return r2.numerator + r2.denominator
    else:
        # Fallback: use numeric best root and rational approximation of r^2
        # Identify which numeric root achieved best_D and compute r^2
        # Recompute to ensure we have the corresponding x
        best_r2 = None
        for xf in pos_real_roots:
            Df = D_from_x_float(xf)
            if abs(Df - best_D) < 1e-10:
                best_r2 = Df / 4.0
                break
        if best_r2 is None:
            # As a safe fallback, take the maximum among numeric candidates
            if pos_real_roots:
                best_r2 = max(D_from_x_float(x)/4.0 for x in pos_real_roots)
            else:
                # No positive roots found; not physically meaningful, return 0
                return 0
        frac_r2 = Fraction(best_r2).limit_denominator(10**9)
        return frac_r2.numerator + frac_r2.denominator

solve(54)

# 调用 solve
result = solve(inputs['surface_area'])
print(result)