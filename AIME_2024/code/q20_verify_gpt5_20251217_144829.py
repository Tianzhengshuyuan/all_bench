inputs = {'size': 5}

def solve(size: int) -> int:
    n = size
    if n <= 0:
        return 0

    # Count pairs of row/column color assignments that yield a maximal configuration.
    # Represent white rows/columns by a bitmask; 1 means white, 0 means black.
    total = 0
    full_mask = (1 << n) - 1

    for rmask in range(1 << n):
        has_white_row = rmask != 0
        has_black_row = rmask != full_mask
        for cmask in range(1 << n):
            has_white_col = cmask != 0
            has_black_col = cmask != full_mask

            # Maximality forces:
            # - no empty rows/columns (else we could add a chip)
            # - each color present among rows iff it is present among columns
            if (has_white_row == has_white_col) and (has_black_row == has_black_col):
                total += 1

    return total

# 调用 solve
result = solve(inputs['size'])
print(result)