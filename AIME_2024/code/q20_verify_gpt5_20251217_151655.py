inputs = {'size': 5}

def solve(size: int) -> int:
    n = size
    if n <= 0:
        return 0

    # Count maximal configurations by choosing sets of white rows (Rw) and white columns (Cw).
    # The board is then uniquely determined: fill all cells in (Rw x Cw) with white, and
    # ((~Rw) x (~Cw)) with black; mismatches are empty. Maximality requires:
    # - no empty rows or columns, which is equivalent to:
    #     (|Rw| > 0) iff (|Cw| > 0) and (|Rw| < n) iff (|Cw| < n).
    # That yields the count: sum_{Rw,Cw} 1 over valid choices.
    # We implement this directly by iterating subsets.

    total = 0
    full_mask = (1 << n) - 1

    for rmask in range(1 << n):
        a = rmask.bit_count()             # number of white rows
        has_white_row = a > 0
        has_black_row = a < n
        for cmask in range(1 << n):
            b = cmask.bit_count()         # number of white columns
            has_white_col = b > 0
            has_black_col = b < n

            # Valid-maximal iff the presence of colors matches between rows and columns
            if (has_white_row == has_white_col) and (has_black_row == has_black_col):
                total += 1

    return total

# 调用 solve
result = solve(inputs['size'])
print(result)