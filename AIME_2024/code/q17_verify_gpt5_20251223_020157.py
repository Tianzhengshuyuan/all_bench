inputs = {'surface_area': 54}

from fractions import Fraction
import math

def solve(surface_area):
    # Given fixed volume
    V = 23
    s = Fraction(surface_area, 2)  # x^2 + 2xy = s with a=b=x, c=y and x^2*y=V
    
    def divisors(n):
        n = abs(int(n))
        res = set()
        for i in range(1, int(math.isqrt(n)) + 1):
            if n % i == 0:
                res.add(i)
                res.add(n // i)
        return sorted(res)
    
    # Find positive rational roots of x^3 - s x + 2V = 0 using Rational Root Theorem
    A = s.denominator
    num = s.numerator
    C = 2 * V * A
    pos_roots = set()
    if A != 0:
        for q in divisors(A):
            for p in divisors(C):
                r = Fraction(p, q)
                if r > 0 and r**3 - s * r + 2 * V == 0:
                    pos_roots.add(r)
    roots = sorted(pos_roots)
    
    # Fallback to numeric Cardano if no rational roots found
    if not roots:
        p = -float(s)
        q = 2.0 * V
        delta = (q / 2) ** 2 + (p / 3) ** 3
        
        def cbrt(x):
            return math.copysign(abs(x) ** (1.0 / 3.0), x)
        
        numeric_roots = []
        if delta > 0:
            A1 = -q / 2 + math.sqrt(delta)
            B1 = -q / 2 - math.sqrt(delta)
            t = cbrt(A1) + cbrt(B1)
            if t > 0:
                numeric_roots.append(t)
        elif abs(delta) < 1e-15:
            t1 = 2 * cbrt(-q / 2)
            t2 = -cbrt(-q / 2)
            if t1 > 0:
                numeric_roots.append(t1)
            if t2 > 0:
                numeric_roots.append(t2)
        else:
            r = 2 * math.sqrt(-p / 3)
            theta = math.acos((-q / 2) / math.sqrt((-p / 3) ** 3))
            for k in range(3):
                t = r * math.cos((theta + 2 * math.pi * k) / 3)
                if t > 0:
                    numeric_roots.append(t)
        roots = numeric_roots
    
    # Compute r^2 = (2x^2 + y^2)/4 with y = V/x^2 and take the maximum over positive roots
    r2_candidates = []
    for x in roots:
        if isinstance(x, Fraction):
            y = Fraction(V, 1) / (x * x)
            r2 = (2 * x * x + y * y) / 4
            r2_candidates.append(r2)
        else:
            y = V / (x * x)
            r2 = (2 * x * x + y * y) / 4.0
            r2_candidates.append(r2)
    
    if not r2_candidates:
        return None  # No feasible solution
    
    r2_max = max(r2_candidates, key=lambda z: float(z))
    
    # Return p+q for r^2 = p/q in lowest terms
    if isinstance(r2_max, Fraction):
        return r2_max.numerator + r2_max.denominator
    else:
        frac = Fraction(r2_max).limit_denominator(10**12)
        return frac.numerator + frac.denominator

solve(54)

# 调用 solve
result = solve(inputs['surface_area'])
print(result)