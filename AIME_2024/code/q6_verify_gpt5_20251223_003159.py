inputs = {'freq_y': 3}

def solve(freq_y):
    import math

    pi = math.pi

    # Piecewise definition of h(x) = 4 g(f(x)) for |x| <= 1
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

    # Count solutions of cos(theta) = val for theta in [0, omega]
    def count_cos_eq(omega, val):
        eps = 1e-12
        if val < -1.0 - 1e-15 or val > 1.0 + 1e-15:
            return 0
        val = max(-1.0, min(1.0, val))
        if omega <= eps:
            return 1 if abs(val - 1.0) <= 1e-12 else 0

        # Special cases val = ±1
        if abs(val - 1.0) <= 1e-12:
            # theta = 0 + 2π n
            return int(math.floor(omega / (2 * pi))) + 1
        if abs(val + 1.0) <= 1e-12:
            # theta = π + 2π n
            if omega + eps < pi:
                return 0
            return int(math.floor((omega - pi) / (2 * pi))) + 1

        alpha = math.acos(val)  # in (0, π)
        # Branch 1: theta = alpha + 2π n
        n_min1 = 0
        n_max1 = int(math.floor((omega - alpha) / (2 * pi)))
        count1 = max(0, n_max1 - n_min1 + 1)

        # Branch 2: theta = 2π - alpha + 2π n
        b = 2 * pi - alpha
        n_min2 = 0
        n_max2 = int(math.floor((omega - b) / (2 * pi)))
        count2 = max(0, n_max2 - n_min2 + 1)

        return count1 + count2

    # Count solutions of |cos(theta)| = c for theta in [0, omega]
    def count_abs_cos(omega, c):
        if c < 0:
            return 0
        if abs(c) <= 1e-15:
            return count_cos_eq(omega, 0.0)
        else:
            return count_cos_eq(omega, c) + count_cos_eq(omega, -c)

    # Waves for q(y) = h(cos(|freq_y| * pi * y)) on y in [0,1]
    omega = abs(freq_y) * pi
    H0_v = count_abs_cos(omega, 0.25) + count_abs_cos(omega, 0.75)
    H1_v = count_abs_cos(omega, 0.0) + count_abs_cos(omega, 0.5) + count_abs_cos(omega, 1.0)
    waves_v = max(0, H0_v + H1_v - 1)

    # Waves for p(x) = h(sin(2π x)) on x in [0,1] (one full period -> 16)
    waves_u = 16

    # Base intersections from crossing of monotone waves
    total = waves_u * waves_v

    # Extra boundary intersection at y = 1 if it coincides with an endpoint of p(x)=1
    x_endpoints = [0.0, 0.25, 0.5, 0.75, 1.0]
    q_at_1 = h(math.cos(omega))
    for xe in x_endpoints:
        if abs(q_at_1 - xe) <= 1e-12:
            total += 1
            break

    return total

freq_y = 3
solve(freq_y)

# 调用 solve
result = solve(inputs['freq_y'])
print(result)