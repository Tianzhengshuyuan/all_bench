inputs = {'volume': 23}

from fractions import Fraction

def solve(volume):
    # Maximize a^2+b^2+c^2 subject to ab+bc+ca=27 and abc=volume.
    # By symmetry and Lagrange multipliers, at optimum two edges are equal: a=b=x, c=y.
    # Then: x^2 + 2xy = 27 and x^2*y = V.
    # Eliminating y gives cubic in x: x^3 - 27x + 2V = 0.
    # For each positive real root x, y = V/x^2, and the squared diagonal is S = 2x^2 + y^2.
    # The required r^2 is max(S)/4 over the positive roots.
    V = Fraction(volume)

    def divisors(n):
        n = abs(n)
        ds = set()
        if n == 0:
            return {0}
        i = 1
        while i * i <= n:
            if n % i == 0:
                ds.add(i)
                ds.add(n // i)
            i += 1
        return ds

    def F(x):
        return x**3 - 27*x + 2*V

    # Try exact rational roots first (Rational Root Theorem)
    roots = []
    twoV = 2 * V
    num, den = twoV.numerator, twoV.denominator
    if num != 0:
        Ps = divisors(abs(num))
        Qs = divisors(den)
        seen = set()
        for p in Ps:
            for q in Qs:
                for s in (1, -1):
                    x = Fraction(s * p, q)
                    if x <= 0:
                        continue
                    if x in seen:
                        continue
                    if F(x) == 0:
                        roots.append(x)
                    seen.add(x)

    # If no rational roots, fall back to numeric roots when feasible (0 < V <= 27)
    if not roots:
        V_float = float(V)
        def f_float(x):
            return x*x*x - 27*x + 2*V_float

        def bisect(a, b, iters=100):
            fa, fb = f_float(a), f_float(b)
            for _ in range(iters):
                m = 0.5*(a+b)
                fm = f_float(m)
                if fm == 0:
                    return m
                if fa * fm <= 0:
                    b, fb = m, fm
                else:
                    a, fa = m, fm
            return 0.5*(a+b)

        if V_float <= 0 or V_float > 27:
            return None  # infeasible set
        # Bracket roots near (0,3) and (3, R)
        eps = 1e-12
        vals = []
        f0 = f_float(eps)
        f3 = f_float(3.0)
        if f0 * f3 <= 0:
            vals.append(bisect(eps, 3.0))
        if f3 == 0:
            vals.append(3.0)
        else:
            R = 4.0
            fr = f_float(R)
            # increase R until sign changes
            while fr * f3 > 0 and R < 1e9:
                R *= 2.0
                fr = f_float(R)
            if f3 * fr <= 0:
                vals.append(bisect(3.0, R))
        # Compute r^2 from numeric roots and approximate as fraction
        best = None
        for x in vals:
            if x <= 0:
                continue
            y = V_float / (x*x)
            S = 2*x*x + y*y
            r2 = S / 4.0
            if best is None or r2 > best:
                best = r2
        if best is None:
            return None
        r2_frac = Fraction(best).limit_denominator(10**12)
        return r2_frac.numerator + r2_frac.denominator

    # From exact roots, compute r^2 exactly and choose the maximum
    best_r2 = None
    for x in roots:
        y = V / (x * x)
        S = 2 * x * x + y * y
        r2 = S / 4
        if best_r2 is None or r2 > best_r2:
            best_r2 = r2
    best_r2 = best_r2.limit_denominator()
    return best_r2.numerator + best_r2.denominator

solve(volume)

# 调用 solve
result = solve(inputs['volume'])
print(result)