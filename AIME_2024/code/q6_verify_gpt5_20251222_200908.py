inputs = {'cos_freq': 3}

def solve(cos_freq):
    import math

    pi = math.pi

    def h(u):
        return abs(4.0 * abs(abs(u) - 0.5) - 1.0)

    def p(x):
        return h(math.sin(2.0 * pi * x))

    def q(y, c):
        return h(math.cos(c * pi * y))

    def G(x, c):
        return q(p(x), c) - x

    c = abs(float(cos_freq))

    # Sampling density chosen proportional to expected number of intersections (~128*c).
    # Use a generous factor to ensure bracketing of all roots.
    N = int(max(4096, 2048 * max(1.0, c)))
    dx = 1.0 / N

    roots = []

    # Tolerances
    tol_val = 1e-12
    tol_x = 1e-10

    # Evaluate G at grid points and detect sign changes
    x0 = 0.0
    g0 = G(x0, c)
    if abs(g0) <= tol_val:
        roots.append(x0)

    for i in range(N):
        x1 = (i + 1) * dx
        g1 = G(x1, c)

        # Exact hit at grid point
        if abs(g1) <= tol_val:
            roots.append(x1)
        # Sign change between x0 and x1
        if g0 * g1 < 0.0:
            lo, hi = x0, x1
            glo, ghi = g0, g1
            # Bisection
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                gm = G(mid, c)
                if abs(gm) <= tol_val:
                    lo = hi = mid
                    break
                if glo * gm < 0.0:
                    hi = mid
                    ghi = gm
                else:
                    lo = mid
                    glo = gm
            roots.append(0.5 * (lo + hi))

        x0, g0 = x1, g1

    # Deduplicate roots within tolerance
    roots.sort()
    unique = []
    for r in roots:
        if not unique or abs(r - unique[-1]) > tol_x:
            unique.append(r)

    return len(unique)

solve(cos_freq)

# 调用 solve
result = solve(inputs['cos_freq'])
print(result)