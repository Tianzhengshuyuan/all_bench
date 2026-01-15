inputs = {'white_count': 88}

from math import comb

def solve(white_count):
    n = 5
    total_cells = n * n
    black_count = total_cells
    ans = 0

    # All-black configuration
    if black_count >= total_cells:
        ans += 1

    # Mixed configurations: choose nonempty proper subsets of rows/columns for white,
    # ensuring required white chips do not exceed availability.
    for r in range(1, n):
        for c in range(1, n):
            white_needed = r * c
            black_needed = (n - r) * (n - c)
            if white_needed <= white_count and black_needed <= black_count:
                ans += comb(n, r) * comb(n, c)

    # All-white configuration
    if white_count >= total_cells:
        ans += 1

    return ans

solve(25)

# 调用 solve
result = solve(inputs['white_count'])
print(result)