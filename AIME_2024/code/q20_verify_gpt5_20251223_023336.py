inputs = {'white_chips': 25}

def solve(white_chips):
    from math import comb

    n = 5
    B = 25  # fixed number of black chips

    def count_covering_matrices(r, c, t):
        # Count r x c 0-1 matrices with exactly t ones,
        # no all-zero rows and no all-zero columns.
        if r == 0 or c == 0:
            return 1 if t == 0 else 0
        if t < 0 or t > r * c:
            return 0
        res = 0
        for i in range(r + 1):
            for j in range(c + 1):
                cells = (r - i) * (c - j)
                if cells < 0:
                    continue
                ways_cells = comb(cells, t) if 0 <= t <= cells else 0
                res += ((-1) ** (i + j)) * comb(r, i) * comb(c, j) * ways_cells
        return res

    ans = 0

    # Case 1: all-black full grid (rW=cW=0)
    # Always feasible with B=25; maximal regardless of white supply.
    ans += 1  # unique placement (all 25 black cells filled)

    # Case 2: both colors present: 1 <= rW,cW <= n-1
    for r in range(1, n):
        for c in range(1, n):
            # Black block (n-r) x (n-c) fits within B=25, so fully filled.
            # White chips occupy an r x c board; to be maximal, we must use t = min(white_chips, r*c)
            t = min(white_chips, r * c)
            # Each white row/column must have at least one white chip to avoid empty rows/columns overall.
            # This is ensured by counting only matrices with no zero rows/columns.
            cnt_white = count_covering_matrices(r, c, t)
            if cnt_white == 0:
                continue
            ans += comb(n, r) * comb(n, c) * cnt_white

    # Case 3: all-white (rW=cW=n). Black block empty.
    # White chips occupy n x n; maximality requires no zero rows/columns.
    t = min(white_chips, n * n)
    cnt_white = count_covering_matrices(n, n, t)
    ans += cnt_white  # choose all rows and columns: comb(5,5)^2 = 1

    return ans

solve(25)

# 调用 solve
result = solve(inputs['white_chips'])
print(result)