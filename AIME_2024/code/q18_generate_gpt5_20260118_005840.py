inputs = {'n': 14}

def solve(n):
    if n < 4 or n % 2 == 1:
        return 0

    chords = []
    classes = [[] for _ in range(n)]

    for a in range(n):
        for b in range(a + 1, n):
            s = (a + b) % n
            idx = len(chords)
            chords.append((a, b, s))
            classes[s].append(idx)

    def between(a, b, x):
        if a < b:
            return a < x < b
        else:
            return x > a or x < b

    def cross_or_touch(idx1, idx2):
        a, b, _ = chords[idx1]
        c, d, _ = chords[idx2]
        S = {a, b, c, d}
        # If they share a vertex, we count it as an intersection (corner on a polygon vertex)
        if len(S) == 3:
            return True
        if len(S) < 3:  # identical or degenerate, shouldn't happen across perpendicular classes
            return False
        # Proper crossing (endpoints alternate on the circle)
        return (between(a, b, c) ^ between(a, b, d)) and (between(c, d, a) ^ between(c, d, b))

    total = 0
    half = n // 2  # shift in s giving perpendicular families
    for s in range(n):
        t = (s + half) % n
        if s < t:
            A = classes[s]
            B = classes[t]
            if len(A) < 2 or len(B) < 2:
                continue

            masks = []
            for idxA in A:
                mask = 0
                for iB, idxB in enumerate(B):
                    if cross_or_touch(idxA, idxB):
                        mask |= (1 << iB)
                masks.append(mask)

            for i in range(len(A)):
                mi = masks[i]
                # Need at least two B chords intersecting this A chord to form rectangles with another A
                if (mi.bit_count() if hasattr(int, "bit_count") else bin(mi).count("1")) < 2:
                    continue
                for j in range(i + 1, len(A)):
                    inter = mi & masks[j]
                    k = inter.bit_count() if hasattr(int, "bit_count") else bin(inter).count("1")
                    if k >= 2:
                        total += k * (k - 1) // 2

    return total

solve(12)

# 调用 solve
result = solve(inputs['n'])
print(result)