inputs = {'volume': 23}

from fractions import Fraction

def solve(volume):
    # Maximize a^2+b^2+c^2 subject to ab+bc+ca=27 and abc=volume.
    # By symmetry, at optimum two edges are equal: a=b=x, c=y.
    # Then: x^2 + 2xy = 27 and x^2*y = V -> eliminate y to get cubic: x^3 - 27x + 2V = 0.
    V = Fraction(volume)

    # Infeasible if V <= 0 or V > 27 (since max abc under ab+bc+ca=27 is at a=b=c=3 giving 27)
    if V <= 0 or V > 27:
        return None

    def F_frac(x):
        return x**3 - 27*x + 2*V

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

    candidates = []

    # Try exact rational roots first (Rational Root Theorem for x^3 - 27x + 2V = 0)
    twoV = 2 * V
    num, den = twoV.numerator, twoV.denominator
    roots_exact = []
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
                    if F_frac(x) == 0:
                        roots_exact.append(x)
                    seen.add(x)

    # From exact roots, compute r^2 exactly
    for x in roots_exact:
        y = V / (x * x)
        if y <= 0:
            continue
        S = 2 * x * x + y * y
        r2 = S / 4
        candidates.append(('exact', r2))

    # Numeric roots via bisection on intervals (0,3) and (3, +inf) when 0 < V <= 27
    def f_float(x):
        return x*x*x - 27.0*x + 2.0*float(V)

    def bisect(a, b, iters=120):
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

    eps = 1e-12
    f0 = f_float(eps)
    f3 = f_float(3.0)

    numeric_roots = []
    if abs(f3) < 1e-15:
        numeric_roots.append(3.0)
    if f0 * f3 <= 0.0:
        numeric_roots.append(bisect(eps, 3.0))

    if f3 < 0.0:
        R = 4.0
        fr = f_float(R)
        while fr < 0.0 and R < 1e9:
            R *= 2.0
            fr = f_float(R)
        if f3 * fr <= 0.0:
            numeric_roots.append(bisect(3.0, R))

    for x in numeric_roots:
        if x <= 0:
            continue
        y = float(V) / (x * x)
        if y <= 0:
            continue
        S = 2.0 * x * x + y * y
        r2 = S / 4.0
        candidates.append(('float', r2))

    if not candidates:
        return None

    # Choose maximal r^2, preferring exact if tied within tolerance
    best_exact = None
    best_float = None
    for typ, r2 in candidates:
        if typ == 'exact':
            if best_exact is None or r2 > best_exact:
                best_exact = r2
        else:
            if best_float is None or r2 > best_float:
                best_float = r2

    if best_exact is not None:
        if best_float is None or float(best_exact) >= best_float - 1e-12:
            r2 = best_exact.limit_denominator()
            return r2.numerator + r2.denominator

    from fractions import Fraction as Fr
    r2_frac = Fr(best_float).limit_denominator(10**12)
    return r2_frac.numerator + r2_frac.denominator

volume = 23
solve(volume)

# 调用 solve
result = solve(inputs['volume'])
print(result)