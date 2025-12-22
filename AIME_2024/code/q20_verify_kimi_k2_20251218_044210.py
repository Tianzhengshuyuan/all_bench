inputs = {'n': 25}

from math import comb

def solve(n):
    # n is the number of available white chips and also of black chips.
    # The grid is 5×5, so side = 5.
    side = 5
    total = 0

    # Only configurations with either all rows active or all columns active (or both) can be maximal.
    for r in range(side + 1):          # number of active rows
        for c in range(side + 1):      # number of active columns
            if r != side and c != side:
                continue
            # Choose row set and column set
            ways_rows = comb(side, r)
            ways_cols = comb(side, c)

            # Iterate over colour counts
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