inputs = {'freq_cos': 3}

def solve(freq_cos):
    import math

    pi = math.pi

    def h(x):
        u = abs(x)
        v = abs(u - 0.5)
        w = abs(v - 0.25)
        return 4.0 * w

    def T(x):
        y = h(math.sin(2.0 * pi * x))
        return h(math.cos(freq_cos * pi * y))

    def F(x):
        return T(x) - x

    # Parameters for root finding
    # Dense grid to capture many oscillations; scales with |freq_cos|
    N = max(200000, int(6000 * (10 + 16 * abs(freq_cos))))
    eps_zero = 1e-12
    dedup_tol = 1e-7

    roots = []

    # Helper to add a root if not duplicate
    def add_root(r):
        if r < 0.0:
            r = 0.0
        if r > 1.0:
            r = 1.0
        if not roots:
            roots.append(r)
            return
        if abs(r - roots[-1]) > dedup_tol:
            roots.append(r)

    # Check endpoints explicitly
    F0 = F(0.0)
    F1 = F(1.0)
    if abs(F0) < eps_zero:
        add_root(0.0)
    # We'll add x=1 later after scan to avoid ordering conflicts

    # Scan grid for sign changes and near-zero points
    x_prev = 0.0
    f_prev = F0
    for i in range(1, N + 1):
        x_curr = i / N
        f_curr = F(x_curr)

        # If exact/near zero at grid point
        if abs(f_curr) < eps_zero:
            add_root(x_curr)
        # Sign change bracket
        if f_prev == 0.0:
            pass
        elif f_prev * f_curr < 0.0:
            a = x_prev
            b = x_curr
            fa = f_prev
            fb = f_curr
            # Bisection
            for _ in range(60):
                m = 0.5 * (a + b)
                fm = F(m)
                if abs(fm) < 1e-14:
                    a = b = m
                    break
                if fa * fm <= 0.0:
                    b = m
                    fb = fm
                else:
                    a = m
                    fa = fm
            add_root(0.5 * (a + b))

        x_prev = x_curr
        f_prev = f_curr

    if abs(F1) < eps_zero:
        add_root(1.0)

    return len(roots)

solve(3)

# 调用 solve
result = solve(inputs['freq_cos'])
print(result)