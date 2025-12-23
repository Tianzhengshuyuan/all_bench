inputs = {'freq_y': 3}

def solve(freq_y):
    import math

    pi = math.pi

    # Base functions
    def f(x):
        return abs(abs(x) - 0.5)

    def g(x):
        return abs(abs(x) - 0.25)

    def h(x):
        return 4.0 * g(f(x))

    def U(x):
        return h(math.sin(2 * pi * x))

    def V(y):
        return h(math.cos(abs(freq_y) * pi * y))

    def G(x):
        return x - V(U(x))

    # Count hits for |cos(omega*y)| = c in y in [0,1]
    def count_cos_eq(omega, val):
        # count theta in [0, omega] with cos(theta) = val
        if val < -1.0 or val > 1.0:
            return 0
        val = max(-1.0, min(1.0, val))
        if omega == 0.0:
            # theta=0 only
            return 1 if abs(val - 1.0) < 1e-15 else 0
        alpha = math.acos(val)  # in [0, pi]
        twopi = 2.0 * pi
        # enumerate solutions theta = ±alpha + 2πn within [0, omega]
        pts = set()
        n_min = int(math.floor((-alpha) / twopi)) - 1
        n_max = int(math.ceil((omega + alpha) / twopi)) + 1
        for n in range(n_min, n_max + 1):
            for s in (-1.0, 1.0):
                theta = s * alpha + twopi * n
                if -1e-12 <= theta <= omega + 1e-12:
                    # quantize to avoid duplicates from floating error
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
    waves_u = 16  # known from structure

    # Build sampling grid for G(x) = x - V(U(x))
    # Choose samples based on expected number of roots ~ waves_u * waves_v
    expected_roots = max(1, waves_u * max(1, waves_v))
    N = int(max(4000, min(2000000, 20 * expected_roots)))  # cap to keep reasonable

    # Critical x where sin(2πx) hits special levels to enrich grid
    specials = [-1.0, -0.75, -0.5, -0.25, 0.0, 0.25, 0.5, 0.75, 1.0]

    def xs_for_sin_eq(val):
        if val < -1.0 or val > 1.0:
            return []
        alpha = math.asin(val)  # in [-pi/2, pi/2]
        thetas = []
        # Solutions in [0, 2π]: theta = alpha mod 2π, and theta = π - alpha
        theta1 = alpha
        if theta1 < 0:
            theta1 += 2 * pi
        theta2 = math.pi - alpha
        # normalize to [0, 2π]
        if theta2 < 0:
            theta2 += 2 * pi
        if theta2 >= 2 * pi:
            theta2 -= 2 * pi
        thetas.append(theta1)
        thetas.append(theta2)
        # unique and map to x
        xs = set()
        for th in thetas:
            if -1e-12 <= th <= 2 * pi + 1e-12:
                x = th / (2 * pi)
                xs.add(max(0.0, min(1.0, x)))
        # Include endpoints for val == 0 (theta=0 and theta=pi give x=0,0.5, plus x=1 later)
        if abs(val) < 1e-15:
            xs.add(0.5)
        return sorted(xs)

    x_points = set()
    x_points.add(0.0)
    x_points.add(1.0)
    for v in specials:
        for xk in xs_for_sin_eq(v):
            x_points.add(xk)
    # Add uniform grid
    dx = 1.0 / N
    for i in range(N + 1):
        x = i * dx
        x_points.add(x)

    # Add small offsets around criticals to help bracketing
    offsets = [0.0, 1e-6, -1e-6]
    x_points_aug = set()
    for x in x_points:
        for off in offsets:
            xx = x + off
            if 0.0 <= xx <= 1.0:
                x_points_aug.add(xx)
    xs = sorted(x_points_aug)

    # Evaluate and bracket roots
    def bisect_root(a, b, fa, fb, max_iter=80):
        # assumes fa*fb <= 0
        left, right = a, b
        fleft, fright = fa, fb
        for _ in range(max_iter):
            mid = 0.5 * (left + right)
            fmid = G(mid)
            if abs(fmid) < 1e-14:
                return mid
            if fleft * fmid <= 0:
                right, fright = mid, fmid
            else:
                left, fleft = mid, fmid
            if right - left < 1e-12:
                return 0.5 * (left + right)
        return 0.5 * (left + right)

    roots = []

    prev_x = xs[0]
    prev_g = G(prev_x)
    # Endpoint root check
    if abs(prev_g) < 1e-12:
        roots.append(prev_x)

    for i in range(1, len(xs)):
        x = xs[i]
        gx = G(x)
        # Check for root at this sample
        if abs(gx) < 1e-12:
            roots.append(x)
        # Bracketed root between prev_x and x
        elif prev_g * gx < 0:
            r = bisect_root(prev_x, x, prev_g, gx)
            roots.append(r)
        prev_x, prev_g = x, gx

    # Deduplicate roots by proximity
    roots.sort()
    unique_roots = []
    tol_merge = 1e-7
    for r in roots:
        if not unique_roots or abs(r - unique_roots[-1]) > tol_merge:
            unique_roots.append(r)

    return len(unique_roots)

solve(freq_y)

# 调用 solve
result = solve(inputs['freq_y'])
print(result)