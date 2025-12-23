inputs = {'n': 3}

import math

def solve(n):
    def h(x):
        return 4.0 * abs(abs(abs(x) - 0.5) - 0.25)

    def count_interior(n_abs, c):
        # count solutions y in [0,1] of cos(n*pi*y) = c for c in (-1,1)
        m_full = int(math.floor(n_abs / 2.0))  # number of full 2π periods in θ = nπy
        r2 = n_abs - 2.0 * m_full              # remaining fraction in [0,2)
        R = r2 * math.pi
        alpha = math.acos(c)
        cnt = 2 * m_full
        eps = 1e-12
        if R + eps >= alpha:
            cnt += 1
        if R + eps >= 2.0 * math.pi - alpha:
            cnt += 1
        return cnt

    n_abs = abs(n)

    # Z0: x=0 occurrences: cos(nπy) in {±1/4, ±3/4}
    Z0 = 0
    for c in (0.25, -0.25, 0.75, -0.75):
        Z0 += count_interior(n_abs, c)

    # Z1: x=1 occurrences: cos(nπy) in {0, ±1/2, ±1}
    Z1_interior = 0
    for c in (0.0, 0.5, -0.5):
        Z1_interior += count_interior(n_abs, c)
    count_pos1 = int(math.floor(n_abs / 2.0) + 1)          # cosθ=1
    count_neg1 = int(math.floor((n_abs + 1.0) / 2.0))      # cosθ=-1
    Z1 = Z1_interior + count_pos1 + count_neg1

    # waves for Q
    wQ = Z0 + Z1 - 1

    # corner correction: add 1 if (x,y) = (Q(1), 1) is at x in {0,1}
    t = math.cos(n_abs * math.pi)
    s = h(t)
    eps = 1e-12
    b = 1 if (abs(s - 0.0) <= eps or abs(s - 1.0) <= eps) else 0

    # P has 16 waves on [0,1]
    return 16 * wQ + b

solve(3)

# 调用 solve
result = solve(inputs['n'])
print(result)