inputs = {'white_chips': 25}

def solve(white_chips):
    from math import comb
    n = 5
    S_w = white_chips
    S_b = 25  # fixed by problem statement

    def count_covering_matrices(r, c, t):
        # Count r x c 0-1 matrices with exactly t ones,
        # with no all-zero rows and no all-zero columns.
        if r == 0 or c == 0:
            return 1 if t == 0 else 0
        if t < 0 or t > r * c:
            return 0
        res = 0
        for i in range(r + 1):
            for j in range(c + 1):
                cells = (r - i) * (c - j)
                ways_cells = comb(cells, t) if 0 <= t <= cells else 0
                res += ((-1) ** (i + j)) * comb(r, i) * comb(c, j) * ways_cells
        return res

    ans = 0

    # All-black configurations (fill the whole grid with black)
    if S_b >= n * n:
        ans += 1

    # Configurations with both colors potentially present: choose r white-rows and c white-columns
    for r in range(1, n):
        for c in range(1, n):
            t_w = min(S_w, r * c)
            cnt_white = count_covering_matrices(r, c, t_w)
            if cnt_white == 0:
                continue
            ans += comb(n, r) * comb(n, c) * cnt_white

    # All-white configurations (no black chips used)
    t_w = min(S_w, n * n)
    ans += count_covering_matrices(n, n, t_w)

    return ans

solve(25)

# 调用 solve
result = solve(inputs['white_chips'])
print(result)