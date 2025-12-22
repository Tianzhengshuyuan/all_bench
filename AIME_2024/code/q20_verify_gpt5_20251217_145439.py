inputs = {'size': 5}

def solve(size: int) -> int:
    n = size
    if n <= 0:
        return 0

    total = 0
    full_mask = (1 << n) - 1

    # Iterate over all assignments of row/column colors:
    # rmask bit i = 1 means row i is white, 0 means black
    # cmask bit j = 1 means column j is white, 0 means black
    for rmask in range(1 << n):
        has_white_row = rmask != 0
        has_black_row = rmask != full_mask
        for cmask in range(1 << n):
            has_white_col = cmask != 0
            has_black_col = cmask != full_mask

            # To be maximal:
            # - every row must have at least one matching column of its color
            # - every column must have at least one matching row of its color
            # This is equivalent to equality of color-presence sets:
            if (has_white_row != has_white_col) or (has_black_row != has_black_col):
                continue

            # Construct the board by filling exactly the matching intersections.
            # A cell (i, j) is filled with white if r_i = c_j = 1,
            # with black if r_i = c_j = 0, otherwise it is empty.
            # Under the above condition, each row and column is nonempty,
            # and every empty cell is a mismatch, so adding a chip there
            # would violate row or column uniformity. Hence the configuration is maximal.
            total += 1

    return total

# 调用 solve
result = solve(inputs['size'])
print(result)