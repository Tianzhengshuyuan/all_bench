inputs = {'surface_area': 54}

def solve(surface_area):
    from fractions import Fraction
    import math

    S = Fraction(surface_area, 1)
    A = S / 2  # ab+bc+ca
    V = Fraction(23, 1)  # given in problem

    def f(x):
        return x**3 - float(A) * x + 2.0 * float(V)

    # Bisection method on [a,b] where f(a)*f(b) <= 0
    def bisect(a, b, tol=1e-14, max_iter=200):
        fa, fb = f(a), f(b)
        if abs(fa) < tol:
            return a
        if abs(fb) < tol:
            return b
        for _ in range(max_iter):
            m = 0.5 * (a + b)
            fm = f(m)
            if abs(fm) < tol:
                return m
            if fa * fm <= 0:
                b, fb = m, fm
            else:
                a, fa = m, fm
        return 0.5 * (a + b)

    roots = []
    c2 = math.sqrt(max(float(A) / 3.0, 0.0))
    f0 = f(0.0)
    fc2 = f(c2) if c2 > 0 else f(1.0)

    # Root in [0, c2]
    if c2 > 0 and f0 * fc2 <= 0:
        r1 = bisect(0.0, c2)
        if r1 > 1e-12:
            roots.append(r1)

    # Root in [c2, R] by expanding R
    start = max(c2, 1e-9)
    fstart = f(start)
    R = max(1.0, start)
    # Ensure we search enough to find sign change if exists
    if fstart < 0:
        while f(R) <= 0 and R < 1e12:
            R *= 2.0
        if f(R) > 0:
            r2 = bisect(start, R)
            if r2 > 1e-12:
                roots.append(r2)
    elif fstart > 0:
        # Try to find a sign change going left a bit if possible
        L = start / 2.0 if start > 0 else 0.0
        if f(L) < 0:
            r2 = bisect(L, start)
            if r2 > 1e-12:
                roots.append(r2)

    # If no roots found (edge cases), try a generic scan with doubling
    if not roots:
        x = 0.0
        fx = f(x)
        step = 1.0
        for _ in range(60):
            nx = x + step
            fnx = f(nx)
            if fx * fnx <= 0:
                r = bisect(x, nx)
                if r > 1e-12:
                    roots.append(r)
            x, fx = nx, fnx
            step *= 2.0

    # Compute s = a+b+c for each positive root x (with b=c=x, a=V/x^2), choose maximizing s
    best_s = None
    for x in roots:
        if x <= 0:
            continue
        y = float(V) / (x * x)
        s = y + 2.0 * x
        if best_s is None or s > best_s:
            best_s = s

    if best_s is None:
        return None  # no feasible solution found

    # r^2 = (1/4) * (s^2 - 2A)
    r2 = 0.25 * (best_s * best_s - 2.0 * float(A))

    # Convert to fraction and return p+q
    frac = Fraction(r2).limit_denominator(10**12)
    return frac.numerator + frac.denominator

solve(54)

# 调用 solve
result = solve(inputs['surface_area'])
print(result)