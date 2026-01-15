inputs = {'r': '\\frac{20\\sqrt{21}}{63}'}

def solve(r):
    import math

    t = float(r)
    t2 = t * t

    def g(N):
        N = float(N)
        P = 0.5 * (N + 9.0)      # p^2
        Q = 0.5 * (N - 9.0)      # q^2
        R = 0.5 * (169.0 - N)    # r^2
        if P < 0 or Q < 0 or R < 0:
            return float('nan')
        return P * Q * R - 4.0 * t2 * (R * Q + R * P + P * Q)

    a = 9.0 + 1e-8
    b = 169.0 - 1e-8

    def find_roots(a, b, steps=12000):
        roots = []
        prev_x = a
        prev_f = g(a)
        dx = (b - a) / steps
        for i in range(1, steps + 1):
            x = a + i * dx
            fx = g(x)
            if math.isfinite(prev_f) and math.isfinite(fx):
                if abs(fx) < 1e-14:
                    roots.append(x)
                elif prev_f * fx < 0:
                    left, right = prev_x, x
                    fl, fr = prev_f, fx
                    for _ in range(100):
                        mid = (left + right) / 2.0
                        fm = g(mid)
                        if abs(fm) < 1e-16:
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
        # deduplicate
        uniq = []
        for r in roots:
            if all(abs(r - u) > 1e-7 for u in uniq):
                uniq.append(r)
        return uniq

    roots = find_roots(a, b)
    if not roots:
        return None

    # Filter to valid range and pick the one closest to an integer; tie-break by smaller value
    candidates = [rt for rt in roots if 9.0 - 1e-6 <= rt <= 169.0 + 1e-6] or roots
    best = min(candidates, key=lambda v: (abs(v - round(v)), v))
    best_int = int(round(best))
    if abs(best - best_int) < 1e-6:
        return best_int
    return best

solve((20 * (21 ** 0.5)) / 63)

# 调用 solve
result = solve(inputs['r'])
print(result)