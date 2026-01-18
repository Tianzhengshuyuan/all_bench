inputs = {'n': 12}

def solve(n):
    # Count rectangles formed by chords (sides or diagonals) of a regular n-gon.
    # Vertices are labeled 0..n-1 around the circle.
    # A rectangle arises from two pairs of parallel chords whose directions are perpendicular.
    # Directions are classified by (i + j) % n for chord (i, j), i < j.
    if n < 4 or n % 2 == 1:
        return 0

    # Build all chords grouped by direction s = (i + j) % n
    dirs = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            s = (i + j) % n
            dirs[s].append((i, j))

    def in_arc(x, a, b):  # open arc from a to b in CCW order on 0..n-1
        if a < b:
            return a < x < b
        else:
            return x > a or x < b

    def cross_strict(seg1, seg2):
        # strict interior intersection (no shared endpoints)
        (a, b) = seg1
        (c, d) = seg2
        if a == c or a == d or b == c or b == d:
            return False
        return in_arc(c, a, b) ^ in_arc(d, a, b)

    def intersects_inclusive(seg1, seg2):
        # inclusive: interior or at shared endpoint
        (a, b) = seg1
        (c, d) = seg2
        if a == c or a == d or b == c or b == d:
            return True
        return cross_strict(seg1, seg2)

    total = 0
    half = n // 2
    for s in range(half):
        t = (s + half) % n
        A_list = dirs[s]
        B_list = dirs[t]
        mA = len(A_list)
        mB = len(B_list)
        if mA < 2 or mB < 2:
            continue
        # Precompute bitmask of B chords intersecting each A chord
        masks = []
        for (a, b) in A_list:
            mask = 0
            for k, (c, d) in enumerate(B_list):
                if intersects_inclusive((a, b), (c, d)):
                    mask |= (1 << k)
            masks.append(mask)
        # For each unordered pair of A chords, count B chords intersecting both
        for i in range(mA):
            mi = masks[i]
            for j in range(i + 1, mA):
                mj = masks[j]
                cnt = (mi & mj)
                # number of B choices that intersect both A_i and A_j
                c = bin(cnt).count("1")
                if c >= 2:
                    total += c * (c - 1) // 2
    return total

# 调用 solve
result = solve(inputs['n'])
print(result)