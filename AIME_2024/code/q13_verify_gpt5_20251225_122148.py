inputs = {'M': 204}

def solve(M):
    import math
    # Constants in hours
    d = 9.0
    two_point_four = 12.0 / 5.0  # 2.4 hours
    # From equations:
    # 9/(s+0.5) + T = M/60
    # 9/(s+2)   + T = 2.4
    # => 13.5 / ((s+0.5)(s+2)) = M/60 - 2.4
    delta = M / 60.0 - two_point_four
    if delta == 0:
        return float('nan')
    K = (27.0 / 2.0) / delta  # (s+0.5)(s+2)
    # Solve s^2 + 2.5 s + 1 - K = 0
    D = 2.25 + 4.0 * K
    if D < 0:
        return float('nan')
    sqrtD = math.sqrt(D)
    s1 = (-2.5 + sqrtD) / 2.0
    s2 = (-2.5 - sqrtD) / 2.0
    s_candidates = [s for s in (s1, s2) if s > 0]
    s = s_candidates[0] if s_candidates else s1
    # Compute T from the second scenario
    T = two_point_four - d / (s + 2.0)
    # Desired N (hours) from the first scenario
    N = d / s + T
    # Clean near-integer results
    rN = round(N)
    if abs(N - rN) < 1e-9:
        return int(rN)
    return N

solve(204)

# 调用 solve
result = solve(inputs['M'])
print(result)