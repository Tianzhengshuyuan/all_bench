inputs = {'freq_y': 6}

def solve(freq_y):
    import math

    k = abs(float(freq_y))
    pi = math.pi
    two_pi = 2 * pi
    eps = 1e-12

    # Helper to count t in [0, L] such that cos t = c
    def count_cos_eq(L, c):
        if abs(c - 1.0) <= eps:
            return int(math.floor(L / two_pi) + 1)
        if abs(c + 1.0) <= eps:
            if L + eps < pi:
                return 0
            return int(math.floor((L - pi) / two_pi) + 1)
        if abs(c) <= eps:
            if L + eps < pi / 2:
                return 0
            return int(math.floor((L - pi / 2) / pi) + 1)
        # general interior case
        alpha = math.acos(c)
        cntA = 0
        if L + eps >= alpha:
            cntA = int(math.floor((L - alpha) / two_pi) + 1)
            if cntA < 0:
                cntA = 0
        cntB = int(math.floor((L + alpha) / two_pi))
        if cntB < 0:
            cntB = 0
        return cntA + cntB

    # Waves for y = h(sin(2π x)) over x in [0,1]
    # Known counts on one period:
    Wp = 16  # from Nx0=8, Nx1=9 -> 8+9-1

    # Waves for x = h(cos(kπ y)) over y in [0,1]
    L = k * pi
    Ny0 = 0
    for c in (0.25, -0.25, 0.75, -0.75):
        Ny0 += count_cos_eq(L, c)

    Ny1 = 0
    for c in (0.0, 0.5, -0.5, 1.0, -1.0):
        Ny1 += count_cos_eq(L, c)

    Wq = Ny0 + Ny1 - 1

    base_intersections = Wp * Wq

    # Extra intersection at corner (1,1) if q passes through (1,1):
    c_at_one = math.cos(k * pi)
    extra = 0
    for v in (0.0, 0.5, -0.5, 1.0, -1.0):
        if abs(c_at_one - v) <= eps:
            extra = 1
            break

    return int(base_intersections + extra)

# 调用 solve
result = solve(inputs['freq_y'])
print(result)