inputs = {'freq_y': 3}

import math

def solve(freq_y):
    def count_on_interval(omega, base_angles):
        per = 2 * math.pi
        eps = 1e-12
        total = 0
        for theta0 in base_angles:
            k_min = math.ceil((-theta0) / per - eps)
            k_max = math.floor((omega - theta0) / per + eps)
            if k_max >= k_min:
                total += (k_max - k_min + 1)
        return total

    def count_abs_cos_eq_a(omega, a):
        eps = 1e-12
        if a < 0 or a > 1:
            return 0
        if abs(a - 1.0) <= eps:
            base = [0.0, math.pi]
        elif abs(a - 0.0) <= eps:
            base = [math.pi / 2, 3 * math.pi / 2]
        else:
            alpha = math.acos(a)
            base = [alpha, math.pi - alpha, math.pi + alpha, 2 * math.pi - alpha]
        return count_on_interval(omega, base)

    def count_abs_sin_eq_a(omega, a):
        eps = 1e-12
        if a < 0 or a > 1:
            return 0
        if abs(a - 1.0) <= eps:
            base = [math.pi / 2, 3 * math.pi / 2]
        elif abs(a - 0.0) <= eps:
            base = [0.0, math.pi]
        else:
            beta = math.asin(a)
            base = [beta, math.pi - beta, math.pi + beta, 2 * math.pi - beta]
        return count_on_interval(omega, base)

    # q(y) = h(cos(pi * freq_y * y))
    freq = abs(freq_y)
    omega_y = math.pi * freq

    # Count boundary hits for q(y) at x in {0,1} i.e., |cos| in {0, 1/4, 1/2, 3/4, 1}
    Nh_q = 0
    for a in [0.25, 0.75, 0.5, 0.0, 1.0]:
        Nh_q += count_abs_cos_eq_a(omega_y, a)

    # y=1 boundary intersection indicator (corner at (1,1) or (0,1))
    c = abs(math.cos(omega_y))
    eps = 1e-12
    e1 = 1 if any(abs(c - s) <= eps for s in [0.0, 0.25, 0.5, 0.75, 1.0]) else 0

    # Number of up/down waves for q
    Sq = Nh_q - e1  # subtract if both endpoints y=0 and y=1 are boundary hits

    # p(x) = h(sin(2*pi*x)), over x in [0,1]
    omega_x = 2 * math.pi
    Nh_p = 0
    for a in [0.25, 0.75, 0.5, 0.0, 1.0]:
        Nh_p += count_abs_sin_eq_a(omega_x, a)

    # For p(x), both endpoints x=0 and x=1 are boundary hits
    Sp = Nh_p - 1

    # Total intersections: each p-wave crosses each q-wave once, plus corner at y=1 if present
    I = Sp * Sq + e1
    return int(I)

solve(freq_y)

# 调用 solve
result = solve(inputs['freq_y'])
print(result)