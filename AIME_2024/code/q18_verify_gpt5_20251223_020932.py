inputs = {'n': 12}

def solve(n):
    if n % 2 == 1 or n < 4:
        return 0

    # Group all chords by direction class s = (i + j) % n
    L = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            s = (i + j) % n
            L[s].append((i, j))

    def between(i, j, x):
        di = (x - i) % n
        dj = (j - i) % n
        return 0 < di < dj

    def intersect(i, j, k, l):
        # chords (i,j) and (k,l) intersect (including endpoints)
        if i == k or i == l or j == k or j == l:
            return True
        return (between(i, j, k) != between(i, j, l)) and (between(k, l, i) != between(k, l, j))

    count = 0
    half = n // 2
    for s in range(half):
        t = (s + half) % n
        A = L[s]
        B = L[t]
        mA = len(A)
        mB = len(B)
        # Precompute intersection matrix
        ints = [[False] * mB for _ in range(mA)]
        for ai, (i, j) in enumerate(A):
            for bi, (k, l) in enumerate(B):
                ints[ai][bi] = intersect(i, j, k, l)
        # For each pair of A-chords, count B-chords intersecting both
        for ai1 in range(mA):
            row1 = ints[ai1]
            for ai2 in range(ai1 + 1, mA):
                row2 = ints[ai2]
                eligible_B = 0
                for bi in range(mB):
                    if row1[bi] and row2[bi]:
                        eligible_B += 1
                count += eligible_B * (eligible_B - 1) // 2

    return count

solve(12)

# 调用 solve
result = solve(inputs['n'])
print(result)