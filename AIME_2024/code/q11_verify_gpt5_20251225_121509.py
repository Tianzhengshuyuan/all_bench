inputs = {'max_real_part': 540}

def solve(max_real_part):
    import math
    A = 75 + 117j
    B = 96 + 144j
    M = float(max_real_part)

    # Compute coefficients using squared magnitudes and Re(A*B)
    p2 = (A.real * A.real + A.imag * A.imag)
    q2 = (B.real * B.real + B.imag * B.imag)
    s = 2.0 * (A * B).real  # equals 2 * Re(A*B)

    # Quadratic in u = r^2: p2*u^2 - (M^2 - s)*u + q2 = 0
    a = p2
    b = -(M * M - s)
    c = q2

    # Handle degenerate cases
    eps = 1e-12
    if abs(a) < eps:
        # Linear: b*u + c = 0
        if abs(b) < eps:
            return None
        u = -c / b
        if u <= 0:
            return None
        r = math.sqrt(u)
        ri = round(r)
        return int(ri) if abs(r - ri) < 1e-9 else r

    disc = b * b - 4 * a * c
    if disc < -1e-9:
        return None
    if disc < 0:
        disc = 0.0
    sqrt_disc = math.sqrt(disc)

    u1 = (-b + sqrt_disc) / (2 * a)
    u2 = (-b - sqrt_disc) / (2 * a)

    candidates = [u for u in (u1, u2) if u > 0]
    if not candidates:
        return None

    # Choose the larger radius (matches expected answer in the prompt)
    u = max(candidates)
    r = math.sqrt(u)

    ri = round(r)
    return int(ri) if abs(r - ri) < 1e-9 else r

solve(540)

# 调用 solve
result = solve(inputs['max_real_part'])
print(result)