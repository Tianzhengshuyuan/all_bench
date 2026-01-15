inputs = {'max_real_part': 540}

def solve(max_real_part):
    y = float(max_real_part)
    A = 19314.0
    C = 29952.0
    B2 = 19296.0 + y * y
    disc = B2 * B2 - 4.0 * A * C
    if disc < 0 and abs(disc) < 1e-12:
        disc = 0.0
    if disc < 0:
        return None
    sqrt_disc = disc ** 0.5
    t1 = (B2 + sqrt_disc) / (2.0 * A)
    t2 = (B2 - sqrt_disc) / (2.0 * A)
    candidates = [t for t in (t1, t2) if t > 0]
    if not candidates:
        return None
    t = max(candidates)
    r = t ** 0.5
    r_int = round(r)
    if abs(r - r_int) < 1e-9:
        r = r_int
    return r

max_real_part = 540
solve(max_real_part)

# 调用 solve
result = solve(inputs['max_real_part'])
print(result)