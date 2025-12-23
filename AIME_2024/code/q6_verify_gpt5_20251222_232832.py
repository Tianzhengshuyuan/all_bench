inputs = {'k_cos': 3}

import math

def solve(k_cos):
    pi = math.pi
    eps = 1e-12

    def h(u):
        ua = abs(u)
        if ua <= 0.25:
            return 1.0 - 4.0 * ua
        elif ua <= 0.5:
            return 4.0 * ua - 1.0
        elif ua <= 0.75:
            return 3.0 - 4.0 * ua
        else:
            return 4.0 * ua - 3.0

    def count_sin_hits(c):
        # Number of x in [0,1] with sin(2πx) = c
        if abs(c) > 1 + eps:
            return 0
        if abs(c) <= eps:
            return 3  # θ = 0, π, 2π
        if abs(abs(c) - 1.0) <= eps:
            return 1  # θ = π/2 or 3π/2
        return 2      # generic

    def count_cos_hits(c, k):
        # Number of y in [0,1] with cos(kπ y) = c
        if abs(c) > 1 + eps:
            return 0
        L = abs(k) * pi
        two_pi = 2.0 * pi
        if abs(c - 1.0) <= eps:
            return int(math.floor(L / two_pi)) + 1
        if abs(c + 1.0) <= eps:
            if L + eps < pi:
                return 0
            return int(math.floor((L - pi) / two_pi)) + 1
        # generic case
        alpha = math.acos(max(-1.0, min(1.0, c)))
        N_full = int(math.floor(L / two_pi))
        r = L - two_pi * N_full
        count = 2 * N_full
        if r + eps >= alpha:
            count += 1
        if r + eps >= (two_pi - alpha):
            count += 1
        return count

    # Counts for p(x) = h(sin(2πx))
    C0_p = [0.25, -0.25, 0.75, -0.75]
    C1_p = [0.0, 0.5, -0.5, 1.0, -1.0]
    N0_p = sum(count_sin_hits(c) for c in C0_p)
    N1_p = sum(count_sin_hits(c) for c in C1_p)
    Np = (N0_p + N1_p) - 1

    # Counts for q(y) = h(cos(kπ y))
    C0_q = [0.25, -0.25, 0.75, -0.75]
    C1_q = [0.0, 0.5, -0.5, 1.0, -1.0]
    N0_q = sum(count_cos_hits(c, k_cos) for c in C0_q)
    N1_q = sum(count_cos_hits(c, k_cos) for c in C1_q)
    Nq = (N0_q + N1_q) - 1

    base = Np * Nq

    # Extra intersection(s) on the top edge y = 1 at x = q(1)
    x_top = h(math.cos(k_cos * pi))
    y_at_x_top = h(math.sin(2.0 * pi * x_top))
    extra = 1 if abs(y_at_x_top - 1.0) <= 1e-12 else 0

    return base + extra

solve(3)

# 调用 solve
result = solve(inputs['k_cos'])
print(result)