inputs = {'minutes_at_s_plus_half': 204}

def solve(minutes_at_s_plus_half):
    import math

    D = 9.0
    T2 = 2.0 + 24.0 / 60.0  # 2 hours 24 minutes = 2.4 hours
    T3 = minutes_at_s_plus_half / 60.0

    A = T3 - T2
    if abs(A) < 1e-12:
        return None

    K = (D * 1.5) / A  # (s+0.5)(s+2) = 13.5 / A
    delta = 2.25 + 4.0 * K
    if delta < 0:
        return None

    sqrt_delta = math.sqrt(delta)
    r1 = (-2.5 + sqrt_delta) / 2.0
    r2 = (-2.5 - sqrt_delta) / 2.0

    candidates = [r for r in (r1, r2) if r > 0 and r + 2 > 0 and r + 0.5 > 0]
    if not candidates:
        return None

    s = max(candidates)
    t = T2 - D / (s + 2.0)
    N = D / s + t

    if abs(N - round(N)) < 1e-9:
        return int(round(N))
    return N

solve(204)

# 调用 solve
result = solve(inputs['minutes_at_s_plus_half'])
print(result)