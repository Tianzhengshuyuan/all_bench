inputs = {'n': 12}

def solve(n):
    # Count rectangles formed by intersections of chords (including sides)
    # of a regular n-gon, whose sides lie along chords and are pairwise perpendicular.
    if n < 4 or n % 2 == 1:
        return 0

    # Build chord classes by s = (i + j) % n, which determines orientation (parallel classes)
    L = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            s = (i + j) % n
            L[s].append((i, j))

    def in_between(a, b, x):
        # True if x lies strictly on the circular arc from a to b in CCW direction
        da = (b - a) % n
        dx = (x - a) % n
        return 0 < dx < da

    def crosses(ch1, ch2):
        a, b = ch1
        c, d = ch2
        # Exclude shared endpoints
        if len({a, b, c, d}) < 4:
            return False
        return in_between(a, b, c) ^ in_between(a, b, d)

    total = 0
    half = n // 2
    for s in range(half):
        t = s + half
        lines_s = L[s]
        lines_t = L[t]
        m = len(lines_t)
        # Precompute which t-lines each s-line crosses
        cross_sets = []
        for ab in lines_s:
            cs = set()
            for j, cd in enumerate(lines_t):
                if crosses(ab, cd):
                    cs.add(j)
            cross_sets.append(cs)
        # For each unordered pair of s-lines, count pairs of t-lines both cross
        for i in range(len(lines_s)):
            for j in range(i + 1, len(lines_s)):
                k = len(cross_sets[i] & cross_sets[j])
                if k >= 2:
                    total += k * (k - 1) // 2
    return total

solve(12)

# 调用 solve
result = solve(inputs['n'])
print(result)