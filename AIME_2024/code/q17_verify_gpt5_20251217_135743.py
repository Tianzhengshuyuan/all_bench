inputs = {'volume': 23}

# coding: utf-8
import math
from fractions import Fraction

def solve(volume):
    # Given surface area = 54 => ab+bc+ca = s = 27
    s = 27
    v = volume

    # We consider boxes with two equal sides: let b=c=x, a=y.
    # Constraints turn into: x^3 - s*x + 2*v = 0
    # For each positive real root x, y = v/x^2, and
    # r^2 = (a^2 + b^2 + c^2)/4 = (y^2 + 2x^2)/4
    # We take the maximum over positive roots (worst-case box).
    
    def cbrt(z):
        if z >= 0:
            return z ** (1.0/3.0)
        else:
            return -((-z) ** (1.0/3.0))

    def cubic_real_roots(p, q):
        # Solve t^3 + p t + q = 0
        # Discriminant Δ = (q/2)^2 + (p/3)^3
        D = (q/2.0)**2 + (p/3.0)**3
        roots = []
        if D > 1e-15:
            # One real root
            A = -q/2.0 + math.sqrt(D)
            B = -q/2.0 - math.sqrt(D)
            t = cbrt(A) + cbrt(B)
            roots.append(t)
        else:
            # Three real roots (Δ <= 0), use trigonometric form
            # r = 2 sqrt(-p/3)
            r = 2.0 * math.sqrt(max(0.0, -p/3.0))
            # cos(phi) = -q/2 / sqrt((-p/3)^3)
            denom = (-p/3.0)**1.5 if -p/3.0 > 0 else 0.0
            if denom == 0:
                # p=0 => t^3 + q = 0
                roots.append(cbrt(-q))
            else:
                cf = max(-1.0, min(1.0, (-q/2.0)/denom))
                phi = math.acos(cf)
                for k in range(3):
                    ang = (phi + 2.0*math.pi*k)/3.0
                    t = r * math.cos(ang)
                    roots.append(t)
        # Deduplicate close roots
        roots_unique = []
        for t in roots:
            if all(abs(t - u) > 1e-9 for u in roots_unique):
                roots_unique.append(t)
        return roots_unique

    # Build cubic: u^3 - s u + 2 v = 0 -> t^3 + p t + q = 0 with p=-s, q=2v
    p = -s
    q = 2.0 * v
    roots = cubic_real_roots(p, q)
    # Filter positive roots
    pos_roots = [u for u in roots if u > 1e-12]

    # Compute candidate r^2 for each positive root
    def r2_from_u(u):
        y = v / (u*u)
        return (y*y + 2.0*u*u) / 4.0

    if not pos_roots:
        return None  # no feasible box (shouldn't happen for positive s,v)

    # Pick the root that maximizes r^2
    r2_vals = [(r2_from_u(u), u) for u in pos_roots]
    r2_max_val, u_argmax = max(r2_vals, key=lambda x: x[0])

    # Try to get exact fraction if u is an integer root (by rational root theorem)
    # Possible integer roots divide 2v
    r2_frac = None
    if isinstance(v, int) or (isinstance(v, float) and abs(v - round(v)) < 1e-12):
        v_int = int(round(v))
        # Generate divisors of |2v|
        N = abs(2*v_int)
        divisors = set()
        for d in range(1, int(math.isqrt(N))+1):
            if N % d == 0:
                divisors.add(d)
                divisors.add(N//d)
        int_roots = []
        for cand in sorted(divisors):
            for sign in (1, -1):
                x = sign * cand
                if x > 0:
                    # Check integer root
                    if x**3 - s*x + 2*v_int == 0:
                        int_roots.append(x)
        # If we found integer positive roots, compute exact r^2 and see if it matches the max
        best_frac = None
        best_val = -1.0
        for x in int_roots:
            # r^2 = ( (v^2 / x^4) + 2 x^2 ) / 4
            term1 = Fraction(v_int*v_int, x**4)
            term2 = Fraction(2*(x**2), 1)
            ssum = term1 + term2
            r2 = ssum / 4
            val = float(r2)
            if val > best_val:
                best_val = val
                best_frac = r2
        if best_frac is not None and abs(best_val - r2_max_val) < 1e-8:
            r2_frac = best_frac

    if r2_frac is None:
        # Fallback: rational approximation (sufficient for the intended volume=23 case we get exact)
        r2_frac = Fraction(r2_max_val).limit_denominator(10**12)

    return r2_frac.numerator + r2_frac.denominator

# Example:
# print(solve(23))  # Expected 721

# 调用 solve
result = solve(inputs['volume'])
print(result)