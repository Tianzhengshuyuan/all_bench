inputs = {'n': 25}

from math import comb

def solve(n):
    side = 5
    total = 0
    # Only configurations with either all rows active or all columns active (or both) can be maximal.
    for r in range(side + 1):
        for c in range(side + 1):
            if r != side and c != side:
                continue
            ways_rows = comb(side, r)
            ways_cols = comb(side, c)
            for wrow in range(r + 1):
                brow = r - wrow
                for wcol in range(c + 1):
                    bcol = c - wcol
                    white_chips = wrow * wcol + brow * bcol
                    black_chips = wrow * bcol + brow * wcol
                    if white_chips <= n and black_chips <= n:
                        total += ways_rows * ways_cols * comb(r, wrow) * comb(c, wcol)
    return total

# 调用 solve
result = solve(inputs['n'])
print(result)