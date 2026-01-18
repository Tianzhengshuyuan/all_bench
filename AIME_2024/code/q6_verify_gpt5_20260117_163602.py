inputs = {'frequency_y': 3}

def solve(frequency_y):
    import math

    pi = math.pi
    twopi = 2 * math.pi
    eps = 1e-12

    def count_ap(L, base, period):
        if base <= L + eps:
            return int(math.floor((L - base + eps) / period) + 1)
        return 0

    def count_cos_eq(c, L):
        # Count solutions of cos(theta) = c for theta in [0, L], inclusive
        if abs(c - 1.0) <= eps:
            return int(math.floor((L + eps) / twopi) + 1)
        if abs(c + 1.0) <= eps:
            if L + eps < math.pi:
                return 0
            return int(math.floor((L - math.pi + eps) / twopi) + 1)

        alpha = math.acos(c)  # in (0, pi)
        cnt = 0
        # theta = alpha + 2πk
        cnt += count_ap(L, alpha, twopi)
        # theta = 2π - alpha + 2πk
        cnt += count_ap(L, twopi - alpha, twopi)
        return cnt

    # p(x) waves on x in [0,1] (sin has one full 2π period)
    Np_waves = 16  # fixed as derived in the solution outline

    # For q(y): theta = |frequency_y| * pi * y, y in [0,1] => theta in [0, L]
    L = abs(frequency_y) * pi

    S0 = [0.25, -0.25, 0.75, -0.75]          # cos theta in {±1/4, ±3/4} -> h(...)=0
    S1 = [0.0, 0.5, -0.5, 1.0, -1.0]         # cos theta in {0, ±1/2, ±1} -> h(...)=1

    Nq_zero = sum(count_cos_eq(c, L) for c in S0)
    Nq_one = sum(count_cos_eq(c, L) for c in S1)

    Nq_waves = Nq_zero + Nq_one - 1

    # Corner correction: add 1 if q(1) hits x=0 or x=1 (i.e., h(cos L) in {0,1})
    cosL = math.cos(L)
    corner_vals = {0.0, 0.5, -0.5, 1.0, -1.0, 0.25, -0.25, 0.75, -0.75}
    corner_hit = any(abs(cosL - v) <= 1e-12 for v in corner_vals)
    C = 1 if corner_hit else 0

    return Np_waves * Nq_waves + C

solve(frequency_y)

# 调用 solve
result = solve(inputs['frequency_y'])
print(result)