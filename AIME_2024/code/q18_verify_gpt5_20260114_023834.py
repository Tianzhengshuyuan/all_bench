inputs = {'n': 12}

def solve(n):
    import math
    if n % 2 == 1:
        return 0
    eps = 1e-9
    V = [(math.cos(2*math.pi*i/n), math.sin(2*math.pi*i/n)) for i in range(n)]
    # Group lines by direction S = (i+j) mod n
    dir_lines = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            S = (i + j) % n
            dir_lines[S].append((i, j))

    def intersect(p1, p2, p3, p4):
        x1, y1 = p1; x2, y2 = p2; x3, y3 = p3; x4, y4 = p4
        r1x, r1y = x2 - x1, y2 - y1
        r2x, r2y = x4 - x3, y4 - y3
        denom = r1x * r2y - r1y * r2x
        if abs(denom) < eps:
            return None
        t = ((x3 - x1) * r2y - (y3 - y1) * r2x) / denom
        return (x1 + t * r1x, y1 + t * r1y)

    def inside_poly(p):
        # Convex, CCW polygon
        for i in range(n):
            x1, y1 = V[i]; x2, y2 = V[(i + 1) % n]
            if (x2 - x1) * (p[1] - y1) - (y2 - y1) * (p[0] - x1) < -eps:
                return False
        return True

    from itertools import combinations
    total = 0
    half = n // 2
    for S in range(n):
        T = (S + half) % n
        if S < T:
            LS = dir_lines[S]
            LT = dir_lines[T]
            if len(LS) < 2 or len(LT) < 2:
                continue
            for (i1, j1), (i2, j2) in combinations(LS, 2):
                P1, P2 = V[i1], V[j1]
                P3, P4 = V[i2], V[j2]
                for (k1, l1), (k2, l2) in combinations(LT, 2):
                    Q1, Q2 = V[k1], V[l1]
                    Q3, Q4 = V[k2], V[l2]
                    a = intersect(P1, P2, Q1, Q2)
                    b = intersect(P1, P2, Q3, Q4)
                    c = intersect(P3, P4, Q1, Q2)
                    d = intersect(P3, P4, Q3, Q4)
                    if a is None or b is None or c is None or d is None:
                        continue
                    if inside_poly(a) and inside_poly(b) and inside_poly(c) and inside_poly(d):
                        total += 1
    return total

solve(n)

# 调用 solve
result = solve(inputs['n'])
print(result)