inputs = {'volume': 23}

from fractions import Fraction

def solve(volume):
    # We need to maximize a^2+b^2+c^2 with ab+bc+ca=27 and abc=V.
    # By symmetry (Lagrange multipliers), at the extremum two edges are equal: set a=b=x, c=y.
    # Then: x^2 + 2xy = 27 and x^2 y = V, which eliminates to cubic: x^3 - 27x + 2V = 0.
    # For each positive real root x, y = V/x^2 and r^2 = (2x^2 + y^2)/4. Take the maximum.
    V = Fraction(volume)

    # Infeasible if V <= 0 or V > 27 (max abc under ab+bc+ca=27 is at a=b=c=3 giving 27)
    if V <= 0 or V > 27:
        return None

    def r2_from_xy(x, y):
        return (2*x*x + y*y) / 4

    # Rational Root Theorem helpers
    def divisors(n):
        n = abs(n)
        ds = set()
        i = 1
        while i * i <= n:
            if n % i == 0:
                ds.add(i)
                ds.add(n // i)
            i += 1
        return ds

    def F_frac(x):
        return x**3 - 27*x + 2*V

    candidates_exact = []

    # Try to find rational roots exactly (Rational Root Theorem for x^3 - 27x + 2V = 0)
    twoV = 2 * V
    num, den = twoV.numerator, twoV.denominator
    if num != 0:
        Ps, Qs = divisors(abs(num)), divisors(den)
        seen = set()
        for p in Ps:
            for q in Qs:
                for s in (1, -1):
                    x = Fraction(s*p, q)
                    if x in seen or x <= 0:
                        continue
                    seen.add(x)
                    if F_frac(x) == 0:
                        y = V / (x*x)
                        if y > 0:
                            candidates_exact.append(r2_from_xy(x, y))

    # If exact candidate(s) exist, choose the maximum
    if candidates_exact:
        best_exact = max(candidates_exact).limit_denominator()
        return best_exact.numerator + best_exact.denominator

    # Fallback: numeric roots via bisection for 0 < V <= 27
    V_float = float(V)

    def f_float(x):
        return x*x*x - 27.0*x + 2.0*V_float

    def bisect(a, b, iters=150):
        fa, fb = f_float(a), f_float(b)
        for _ in range(iters):
            m = 0.5*(a+b)
            fm = f_float(m)
            if fm == 0.0:
                return m
            if fa * fm <= 0.0:
                b, fb = m, fm
            else:
                a, fa = m, fm
        return 0.5*(a+b)

    numeric_r2_best = None

    # Roots lie in (0,3) and (3, +inf) for V<27; handle V=27 with root at x=3
    eps = 1e-12
    f0 = f_float(eps)
    f3 = f_float(3.0)

    # Left interval (0,3]
    if f0 * f3 < 0.0:
        x = bisect(eps, 3.0)
        y = V_float / (x*x)
        if y > 0:
            r2 = (2.0*x*x + y*y) / 4.0
            numeric_r2_best = r2
    elif abs(f3) < 1e-14:
        x = 3.0
        y = V_float / 9.0
        r2 = (2.0*x*x + y*y) / 4.0
        numeric_r2_best = r2

    # Right interval [3, R)
    if f3 < 0.0:
        R = 4.0
        fr = f_float(R)
        while fr < 0.0 and R < 1e12:
            R *= 2.0
            fr = f_float(R)
        if f3 * fr <= 0.0:
            x = bisect(3.0, R)
            y = V_float / (x*x)
            if y > 0:
                r2 = (2.0*x*x + y*y) / 4.0
                if numeric_r2_best is None or r2 > numeric_r2_best:
                    numeric_r2_best = r2

    if numeric_r2_best is None:
        return None

    r2_frac = Fraction(numeric_r2_best).limit_denominator(10**12)
    return r2_frac.numerator + r2_frac.denominator

volume = 23
solve(volume)

# 调用 solve
result = solve(inputs['volume'])
print(result)