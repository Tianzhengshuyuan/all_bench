inputs = {'surface_area': 94}

from fractions import Fraction
from sympy import symbols, solve, simplify, Rational, sqrt, cbrt, cos, acos, pi, I
from sympy import real_roots, Poly
import math

def solve_exact(surface_area):
    V = 23  # fixed volume from the problem
    S = surface_area

    # Try rational root theorem first
    def divisors(n):
        n = abs(int(n))
        ds = set()
        for i in range(1, int(n**0.5) + 1):
            if n % i == 0:
                ds.add(i)
                ds.add(n // i)
        return sorted(ds)

    roots = []
    if isinstance(S, int):
        A = 2
        C = -S
        D = 4 * V
        p_divs = divisors(D)
        q_divs = divisors(A)
        for p in p_divs:
            for q in q_divs:
                for sign in (-1, 1):
                    cand = Fraction(sign * p, q)
                    val = Fraction(A) * cand**3 + Fraction(C) * cand + Fraction(D)
                    if val == 0:
                        if cand > 0:
                            roots.append(Rational(cand))

    if roots:
        # Use exact Fraction arithmetic
        best_r2 = None
        for a in roots:
            a_frac = Fraction(a.numerator, a.denominator) if isinstance(a, Rational) else a
            d2 = 2 * (a_frac * a_frac) + (Fraction(V, 1) ** 2) / (a_frac ** 4)
            r2 = d2 / 4
            if best_r2 is None or r2 > best_r2:
                best_r2 = r2
        return best_r2.numerator + best_r2.denominator
    else:
        # Use sympy for symbolic solving
        a = symbols('a', real=True, positive=True)
        
        # Solve: 2a^3 - S*a + 4V = 0
        # Or equivalently: a^3 + p*a + q = 0 where p = -S/2, q = 2V
        p = Rational(-S, 2)
        q = Rational(2 * V)
        
        # Equation: a^3 + p*a + q = 0
        eq = a**3 + p*a + q
        
        # Try to find real roots symbolically
        try:
            # Use real_roots for exact representation
            sympy_roots = real_roots(eq)
            if sympy_roots:
                best_r2 = None
                for a_root in sympy_roots:
                    if a_root > 0:
                        # Calculate r^2 = (2a^2 + V^2/a^4) / 4
                        a_val = a_root
                        a_sq = a_val * a_val
                        a_4 = a_sq * a_sq
                        d2 = 2 * a_sq + Rational(V*V) / a_4
                        r2 = d2 / 4
                        
                        # Try to convert to Fraction if it's rational
                        try:
                            r2_frac = Fraction(str(r2))
                            if best_r2 is None or r2_frac > best_r2:
                                best_r2 = r2_frac
                        except:
                            # If not rational, evaluate numerically and convert
                            r2_float = float(r2.evalf())
                            r2_frac = Fraction(r2_float).limit_denominator(10**12)
                            if best_r2 is None or r2_frac > best_r2:
                                best_r2 = r2_frac
                
                if best_r2 is not None:
                    return best_r2.numerator + best_r2.denominator
        except:
            pass
        
        # Fallback to numeric with high precision
        p_float = -S / 2.0
        q_float = 2.0 * V
        delta = (q_float / 2.0) ** 2 + (p_float / 3.0) ** 3

        def cbrt_float(x):
            return math.copysign(abs(x) ** (1.0 / 3.0), x)

        real_roots_list = []
        if delta > 0:
            u = cbrt_float(-q_float / 2.0 + math.sqrt(delta))
            v = cbrt_float(-q_float / 2.0 - math.sqrt(delta))
            x = u + v
            if x > 0:
                real_roots_list.append(x)
        else:
            r = math.sqrt(- (p_float / 3.0) ** 3) if p_float != 0 else 0.0
            if r == 0:
                x = cbrt_float(-q_float)
                if x > 0:
                    real_roots_list.append(x)
            else:
                phi = math.acos(max(-1.0, min(1.0, -q_float / (2.0 * r))))
                m = 2.0 * math.sqrt(-p_float / 3.0)
                for k in range(3):
                    x = m * math.cos((phi + 2 * math.pi * k) / 3.0)
                    if x > 0:
                        real_roots_list.append(x)

        # Deduplicate
        uniq_roots = []
        for x in real_roots_list:
            if not any(abs(x - y) < 1e-12 for y in uniq_roots):
                uniq_roots.append(x)

        max_r2 = None
        for a_val in uniq_roots:
            d2 = 2 * (a_val * a_val) + (V * V) / (a_val ** 4)
            r2 = d2 / 4.0
            if max_r2 is None or r2 > max_r2:
                max_r2 = r2

        if max_r2 is None:
            return None

        frac_r2 = Fraction(max_r2).limit_denominator(10**12)
        return frac_r2.numerator + frac_r2.denominator

# 调用 solve
result = solve_exact(inputs['surface_area'])
print(result)

