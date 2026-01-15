inputs = {'n': 12}

def solve(n):
    import math
    from itertools import combinations

    if n % 4 != 0:
        return 0

    eps = 1e-9
    V = [(math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n)) for i in range(n)]

    # Group chords (segments) by direction class S = (i + j) % n
    dir_segs = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            s = (i + j) % n
            dir_segs[s].append((i, j))

    def cross(ax, ay, bx, by):
        return ax * by - ay * bx

    def sub(p, q):
        return (p[0] - q[0], p[1] - q[1])

    def intersect(p1, p2, p3, p4):
        # Line p1p2 with p3p4
        r = sub(p2, p1)
        s = sub(p4, p3)
        denom = cross(r[0], r[1], s[0], s[1])
        if abs(denom) < eps:
            return None
        t = cross(sub(p3, p1)[0], sub(p3, p1)[1], s[0], s[1]) / denom
        return (p1[0] + t * r[0], p1[1] + t * r[1])

    def on_segment(p, a, b):
        # Check if p is on segment ab (inclusive)
        ax, ay = a
        bx, by = b
        px, py = p
        # Colinearity
        if abs(cross(bx - ax, by - ay, px - ax, py - ay)) > eps:
            return False
        # Within bounding box
        if (min(ax, bx) - eps <= px <= max(ax, bx) + eps) and (min(ay, by) - eps <= py <= max(ay, by) + eps):
            return True
        return False

    def dist2(p, q):
        dx = p[0] - q[0]
        dy = p[1] - q[1]
        return dx * dx + dy * dy

    total = 0
    quarter = n // 4
    for s in range(n):
        t = (s + quarter) % n  # perpendicular direction class
        if s < t:
            LS = dir_segs[s]
            LT = dir_segs[t]
            if len(LS) < 2 or len(LT) < 2:
                continue
            for (i1, j1), (i2, j2) in combinations(LS, 2):
                A1, A2 = V[i1], V[j1]
                B1, B2 = V[i2], V[j2]
                for (k1, l1), (k2, l2) in combinations(LT, 2):
                    C1, C2 = V[k1], V[l1]
                    D1, D2 = V[k2], V[l2]
                    a = intersect(A1, A2, C1, C2)
                    b = intersect(A1, A2, D1, D2)
                    c = intersect(B1, B2, C1, C2)
                    d = intersect(B1, B2, D1, D2)
                    if a is None or b is None or c is None or d is None:
                        continue
                    # Each vertex must lie on both relevant segments
                    if not (on_segment(a, A1, A2) and on_segment(a, C1, C2)):
                        continue
                    if not (on_segment(b, A1, A2) and on_segment(b, D1, D2)):
                        continue
                    if not (on_segment(c, B1, B2) and on_segment(c, C1, C2)):
                        continue
                    if not (on_segment(d, B1, B2) and on_segment(d, D1, D2)):
                        continue
                    # Non-degenerate (positive side lengths)
                    if dist2(a, b) <= eps or dist2(a, c) <= eps:
                        continue
                    total += 1
    return total

solve(12)

# 调用 solve
result = solve(inputs['n'])
print(result)