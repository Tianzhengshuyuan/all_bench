inputs = {'R': 315}

def solve(R):
    import math

    def comb2(k):
        return k * (k - 1) // 2 if k >= 2 else 0

    def count_rectangles(n):
        if n < 4 or n % 2 == 1:
            return 0

        # generate vertices on unit circle
        verts = [(math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n)) for i in range(n)]

        # group all segments (sides and diagonals) by direction index m = (i + j) % n
        # store each segment as (p, q, A, B, C) for line Ax + By + C = 0
        segs_by_dir = [[] for _ in range(n)]
        for i in range(n):
            x1, y1 = verts[i]
            for j in range(i + 1, n):
                x2, y2 = verts[j]
                # line coefficients
                A = y1 - y2
                B = x2 - x1
                C = x1 * y2 - x2 * y1
                m = (i + j) % n
                segs_by_dir[m].append((x1, y1, x2, y2, A, B, C))

        eps = 1e-9

        def intersect_on_segments(seg1, seg2):
            x1, y1, x2, y2, A1, B1, C1 = seg1
            x3, y3, x4, y4, A2, B2, C2 = seg2
            D = A1 * B2 - A2 * B1
            if abs(D) < eps:
                return False
            # intersection of lines
            x = (B1 * C2 - B2 * C1) / D
            y = (C1 * A2 - C2 * A1) / D

            # check if intersection lies within segment 1
            vx1 = x2 - x1
            vy1 = y2 - y1
            denom1 = vx1 * vx1 + vy1 * vy1
            t1 = ((x - x1) * vx1 + (y - y1) * vy1) / denom1
            if not (-eps <= t1 <= 1 + eps):
                return False

            # check if intersection lies within segment 2
            vx2 = x4 - x3
            vy2 = y4 - y3
            denom2 = vx2 * vx2 + vy2 * vy2
            t2 = ((x - x3) * vx2 + (y - y3) * vy2) / denom2
            if not (-eps <= t2 <= 1 + eps):
                return False

            return True

        total = 0
        half = n // 2
        # process each unordered perpendicular direction pair (m, m+half)
        for m in range(half):
            A = segs_by_dir[m]
            B = segs_by_dir[(m + half) % n]
            if not A or not B:
                continue

            # build bitmask rows: for each segment in A, which segments in B intersect on segments
            masks = []
            for segA in A:
                mask = 0
                for j, segB in enumerate(B):
                    if intersect_on_segments(segA, segB):
                        mask |= (1 << j)
                masks.append(mask)

            # count 2x2 all-ones submatrices via pairwise row intersections
            L = len(masks)
            for i in range(L):
                mi = masks[i]
                if mi == 0:
                    continue
                for k in range(i + 1, L):
                    c = (mi & masks[k]).bit_count()
                    total += comb2(c)

        return total

    # search for n such that count_rectangles(n) == R
    # choose a reasonable upper bound for n
    max_n = 100
    for n in range(3, max_n + 1):
        if count_rectangles(n) == R:
            return n
    return None

solve(R)

# 调用 solve
result = solve(inputs['R'])
print(result)