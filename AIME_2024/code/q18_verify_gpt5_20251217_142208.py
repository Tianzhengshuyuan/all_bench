inputs = {'n_sides': 6}

def solve(n_sides: int) -> int:
    n = n_sides
    if n % 2 == 1:
        return 0  # No perpendicular classes among chord directions
    
    # Generate all chords (i, j) with 0 <= i < j < n
    chords = []
    for i in range(n):
        for j in range(i + 1, n):
            s = (i + j) % n  # orientation class by sum of indices mod n
            chords.append((i, j, s))
    
    # Group chords by their orientation class s
    groups = {s: [] for s in range(n)}
    for (i, j, s) in chords:
        groups[s].append((i, j))
    
    def intersects(a, b):
        # a: (i, j), b: (k, l), with i<j and k<l
        i, j = a
        k, l = b
        # share endpoint counts as intersection
        if i == k or i == l or j == k or j == l:
            return True
        # strict interior intersection when endpoints interleave
        def between(x, y, z):
            return x < z < y
        inter1 = between(i, j, k)
        inter2 = between(i, j, l)
        inter3 = between(k, l, i)
        inter4 = between(k, l, j)
        return (inter1 != inter2) and (inter3 != inter4)
    
    def popcount(x: int) -> int:
        try:
            return x.bit_count()
        except AttributeError:
            return bin(x).count("1")
    
    total = 0
    half = n // 2
    # Process each perpendicular pair (s, s+half) once
    for s in range(half):
        sp = (s + half) % n
        A = groups[s]
        B = groups[sp]
        if len(A) < 2 or len(B) < 2:
            continue
        
        # Precompute intersection masks of chords in A against list B
        # Map B chords to indices
        b_index = {idx: idx for idx in range(len(B))}  # identity mapping for enumeration
        # Build masks: for each a in A, a_mask over B chords
        a_masks = []
        for (ai, aj) in A:
            mask = 0
            for bi, (bk, bl) in enumerate(B):
                if intersects((ai, aj), (bk, bl)):
                    mask |= (1 << bi)
            a_masks.append(mask)
        
        # For each unordered pair of chords in A, count common B intersections
        m = len(A)
        for u in range(m):
            mu = a_masks[u]
            if mu == 0:
                continue
            for v in range(u + 1, m):
                mv = a_masks[v]
                t = popcount(mu & mv)
                if t >= 2:
                    total += t * (t - 1) // 2
    
    return total

# 调用 solve
result = solve(inputs['n_sides'])
print(result)