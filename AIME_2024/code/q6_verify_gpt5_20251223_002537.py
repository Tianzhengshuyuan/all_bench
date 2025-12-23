inputs = {'freq_y': 3}

def solve(freq_y):
    import math

    pi = math.pi

    # Fast piecewise h(x) = 4 g(f(x)) for x in [-1,1]
    def h(x):
        a = abs(x)
        if a <= 0.25:
            return 1.0 - 4.0 * a
        elif a <= 0.5:
            return 4.0 * a - 1.0
        elif a <= 0.75:
            return 3.0 - 4.0 * a
        else:
            return 4.0 * a - 3.0

    def U(x):
        return h(math.sin(2 * pi * x))

    def V(y):
        return h(math.cos(abs(freq_y) * pi * y))

    def G(x):
        return x - V(U(x))

    # Count hits for |cos(omega*y)| = c in y in [0,1] to estimate complexity
    def count_cos_eq(omega, val):
        if val < -1.0 or val > 1.0:
            return 0
        if omega == 0.0:
            return 1 if abs(val - 1.0) < 1e-15 else 0
        alpha = math.acos(max(-1.0, min(1.0, val)))  # in [0, pi]
        twopi = 2.0 * pi
        pts = set()
        # enumerate solutions theta = ±alpha + 2πn within [0, omega]
        n_min = int(math.floor((-alpha) / twopi)) - 1
        n_max = int(math.ceil((omega + alpha) / twopi)) + 1
        for n in range(n_min, n_max + 1):
            for s in (-1.0, 1.0):
                theta = s * alpha + twopi * n
                if -1e-12 <= theta <= omega + 1e-12:
                    key = int(round(theta / 1e-12))
                    pts.add(key)
        return len(pts)

    def count_abs_cos(omega, c):
        if omega == 0.0:
            return 1 if abs(c - 1.0) < 1e-15 else 0
        if c < 0:
            return 0
        if abs(c) < 1e-15:
            return count_cos_eq(omega, 0.0)
        else:
            return count_cos_eq(omega, c) + count_cos_eq(omega, -c)

    omega = abs(freq_y) * pi

    # Count boundary hits for V(y)
    H0_v = count_abs_cos(omega, 0.25) + count_abs_cos(omega, 0.75)
    H1_v = count_abs_cos(omega, 0.0) + count_abs_cos(omega, 0.5) + count_abs_cos(omega, 1.0)
    waves_v = max(0, H0_v + H1_v - 1)

    # For U(x) on x in [0,1], it's fixed (one period)
    waves_u = 16

    # Set dense sampling to robustly capture all roots (including near-tangential)
    expected_roots = max(1, waves_u * max(1, waves_v))
    N = int(max(100000, min(2000000, 600 * expected_roots)))

    # Enrich grid at critical sin levels
    specials = [-1.0, -0.75, -0.5, -0.25, 0.0, 0.25, 0.5, 0.75, 1.0]

    def xs_for_sin_eq(val):
        if val < -1.0 or val > 1.0:
            return []
        alpha = math.asin(val)
        thetas = []
        theta1 = alpha
        if theta1 < 0:
            theta1 += 2 * pi
        theta2 = math.pi - alpha
        if theta2 < 0:
            theta2 += 2 * pi
        if theta2 >= 2 * pi:
            theta2 -= 2 * pi
        thetas.append(theta1)
        thetas.append(theta2)
        xs = set()
        for th in thetas:
            if -1e-12 <= th <= 2 * pi + 1e-12:
                x = th / (2 * pi)
                xs.add(max(0.0, min(1.0, x)))
        if abs(val) < 1e-15:
            xs.add(0.5)
        return sorted(xs)

    x_points = set([0.0, 1.0])
    for v in specials:
        for xk in xs_for_sin_eq(v):
            x_points.add(xk)

    # Uniform grid
    dx = 1.0 / N
    for i in range(N + 1):
        x_points.add(i * dx)

    # Add small offsets around criticals
    offsets = [0.0, 1e-5, -1e-5, 3e-5, -3e-5]
    x_points_aug = set()
    for x in x_points:
        for off in offsets:
            xx = x + off
            if 0.0 <= xx <= 1.0:
                x_points_aug.add(xx)
    xs = sorted(x_points_aug)

    # Evaluate G on grid
    gs = [G(x) for x in xs]

    # Root bracketing and near-zero detection
    tol_zero = 1e-12
    tol_near = 2e-6
    candidates = []

    def bisect_root(a, b, fa, fb, max_iter=100):
        left, right = a, b
        fleft, fright = fa, fb
        for _ in range(max_iter):
            mid = 0.5 * (left + right)
            fmid = G(mid)
            if abs(fmid) < 1e-14 or right - left < 1e-12:
                return mid
            if fleft * fmid <= 0:
                right, fright = mid, fmid
            else:
                left, fleft = mid, fmid
        return 0.5 * (left + right)

    # Endpoint check
    if abs(gs[0]) < tol_near:
        candidates.append(xs[0])

    for i in range(1, len(xs)):
        a, b = xs[i - 1], xs[i]
        fa, fb = gs[i - 1], gs[i]

        if abs(fb) < tol_near:
            candidates.append(b)
            continue

        if fa * fb < 0:
            r = bisect_root(a, b, fa, fb)
            candidates.append(r)
        else:
            # Near-zero within interval by local minima detection
            if min(abs(fa), abs(fb)) < tol_near:
                # take closer endpoint
                candidates.append(a if abs(fa) <= abs(fb) else b)

    # Triple-point local minima detection to catch tangential zeros
    for i in range(1, len(xs) - 1):
        if abs(gs[i]) <= min(abs(gs[i - 1]), abs(gs[i + 1])) and abs(gs[i]) < tol_near:
            candidates.append(xs[i])

    # Deduplicate
    candidates.sort()
    unique_roots = []
    tol_merge = 1e-5
    for r in candidates:
        if not unique_roots or abs(r - unique_roots[-1]) > tol_merge:
            unique_roots.append(r)

    return len(unique_roots)

freq_y = 3
solve(freq_y)

# 调用 solve
result = solve(inputs['freq_y'])
print(result)