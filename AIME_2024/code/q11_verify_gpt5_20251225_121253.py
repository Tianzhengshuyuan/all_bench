inputs = {'max_real_part': 540}

def solve(max_real_part):
    import math
    A = 75 + 117j
    B = 96 + 144j
    p = abs(A)
    q = abs(B)
    M = float(max_real_part)

    if p == 0:
        if M <= 0:
            return None
        r = q / M
        ri = round(r)
        return int(ri) if abs(r - ri) < 1e-9 else r

    disc = M * M - 4 * p * q
    if disc < -1e-12:
        return None
    if disc < 0:
        disc = 0.0

    sqrt_disc = math.sqrt(disc)
    denom = 2 * p
    r1 = (M + sqrt_disc) / denom
    r2 = (M - sqrt_disc) / denom

    candidates = [r for r in (r1, r2) if r > 0]
    if not candidates:
        return None
    r = max(candidates)

    ri = round(r)
    return int(ri) if abs(r - ri) < 1e-9 else r

solve(max_real_part)

# 调用 solve
result = solve(inputs['max_real_part'])
print(result)