inputs = {'r': '\\frac{20\\sqrt{21}}{63}'}

def solve(r):
    import math

    R = float(r) * float(r)

    def F(N):
        N = float(N)
        # A(N) / B(N) = R with constants from the problem (AC^2=80, AD^2=89)
        # A(N) = (N^2 - 81)(169 - N)
        # B(N) = 8(-N^2 + 338N - 81)
        A = (N * N - 81.0) * (169.0 - N)
        B = 8.0 * (-N * N + 338.0 * N - 81.0)
        return R - (A / B)

    def find_roots(intervals, steps=5000):
        roots = []
        for a, b in intervals:
            fa = F(a)
            prev_x, prev_f = a, fa
            dx = (b - a) / steps
            for i in range(1, steps + 1):
                x = a + i * dx
                fx = F(x)
                if abs(fx) < 1e-14:
                    roots.append(x)
                elif prev_f * fx < 0:
                    left, right = prev_x, x
                    fl, fr = prev_f, fx
                    for _ in range(80):
                        mid = (left + right) / 2.0
                        fm = F(mid)
                        if abs(fm) < 1e-14:
                            left = right = mid
                            break
                        if fl * fm <= 0:
                            right = mid
                            fr = fm
                        else:
                            left = mid
                            fl = fm
                    roots.append((left + right) / 2.0)
                prev_x, prev_f = x, fx
        # deduplicate close roots
        roots_sorted = []
        for rt in roots:
            if not any(abs(rt - s) < 1e-7 for s in roots_sorted):
                roots_sorted.append(rt)
        return roots_sorted

    # Search in natural sub-intervals and pick the smaller root,
    # which corresponds to the smaller N (e.g., 41 for the given r).
    eps = 1e-6
    intervals = [(9.0 + eps, 80.0 - eps), (80.0 + eps, 169.0 - eps)]
    roots = find_roots(intervals, steps=6000)
    if not roots:
        roots = find_roots([(9.0 + eps, 169.0 - eps)], steps=12000)
    if not roots:
        return None
    N_val = min(roots)
    N_round = round(N_val)
    if abs(N_val - N_round) < 1e-9:
        return int(N_round)
    return N_val

solve(r)

# 调用 solve
result = solve(inputs['r'])
print(result)