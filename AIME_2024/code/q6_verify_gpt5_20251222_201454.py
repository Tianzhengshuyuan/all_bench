inputs = {'cos_freq': 3}

def solve(cos_freq):
    import math

    pi = math.pi
    tau = 2.0 * pi
    eps = 1e-12

    def count_abs_cos_hits(L, a):
        # Count theta in [0, L] such that |cos(theta)| = a
        a = float(a)
        if a < 0.0:
            return 0
        if a > 1.0:
            return 0

        # Generate base offsets in [0, 2*pi)
        if abs(a - 1.0) <= eps:
            deltas = [0.0, pi]
        elif abs(a) <= eps:
            deltas = [0.5 * pi, 1.5 * pi]
        else:
            alpha = math.acos(a)
            deltas = [alpha, pi - alpha, pi + alpha, tau - alpha]

        # Deduplicate deltas within tolerance
        deltas = sorted(deltas)
        uniq = []
        for d in deltas:
            if not uniq or abs(d - uniq[-1]) > 1e-12:
                uniq.append(d)

        cnt = 0
        for d in uniq:
            if d <= L + eps:
                cnt += 1 + int(math.floor((L - d + eps) / tau))
        return cnt

    # Counts for P(x) = H(sin(2*pi*x)) over x in [0,1] (theta in [0, 2*pi])
    Lp = tau
    N1P = (
        count_abs_cos_hits(Lp, 1.0) +
        count_abs_cos_hits(Lp, 0.5) +
        count_abs_cos_hits(Lp, 0.0)
    )
    N0P = (
        count_abs_cos_hits(Lp, 0.25) +
        count_abs_cos_hits(Lp, 0.75)
    )
    Wp = N1P + N0P - 1  # number of monotone waves of P

    # Counts for Q(y) = H(cos(c*pi*y)) over y in [0,1] (theta in [0, c*pi])
    c = abs(float(cos_freq))
    Lq = c * pi
    N1Q = (
        count_abs_cos_hits(Lq, 1.0) +
        count_abs_cos_hits(Lq, 0.5) +
        count_abs_cos_hits(Lq, 0.0)
    )
    N0Q = (
        count_abs_cos_hits(Lq, 0.25) +
        count_abs_cos_hits(Lq, 0.75)
    )
    Wq = N1Q + N0Q - 1  # number of monotone waves of Q

    base = Wp * Wq

    # Extra corner intersection at (1,1) when Q(1) = 1, i.e. |cos(c*pi)| in {0, 1/2, 1}
    u = abs(math.cos(Lq))
    delta = 1 if (abs(u - 1.0) <= eps or abs(u - 0.5) <= eps or abs(u - 0.0) <= eps) else 0

    return int(base + delta)

solve(3)

# 调用 solve
result = solve(inputs['cos_freq'])
print(result)