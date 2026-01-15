inputs = {'time_minutes_s_plus_half': 204}

def solve(time_minutes_s_plus_half):
    M = float(time_minutes_s_plus_half)
    delta = M - 144.0
    if abs(delta) < 1e-12:
        return float('nan')
    X = 810.0 / delta
    D = 2.25 + 4.0 * X
    if D < 0:
        return float('nan')
    sqrtD = D ** 0.5
    r1 = (-2.5 + sqrtD) / 2.0
    r2 = (-2.5 - sqrtD) / 2.0
    s_candidates = [r1, r2]
    s_valid = [r for r in s_candidates if r > 0]
    s = max(s_valid) if s_valid else max(s_candidates)
    if abs(s + 2.0) < 1e-12 or abs(s + 0.5) < 1e-12 or abs(s) < 1e-12:
        return float('nan')
    t = 144.0 - 540.0 / (s + 2.0)
    total_minutes_at_s = 540.0 / s + t
    N_hours = total_minutes_at_s / 60.0
    if abs(N_hours - round(N_hours)) < 1e-9:
        return int(round(N_hours))
    return N_hours

solve(204)

# 调用 solve
result = solve(inputs['time_minutes_s_plus_half'])
print(result)