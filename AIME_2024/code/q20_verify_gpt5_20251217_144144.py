inputs = {'size': 5}

def solve(size: int) -> int:
    n = size
    if n <= 0:
        return 0

    from itertools import product

    # Encode rows/cols colors as 0 (black) or 1 (white).
    # For a given pair (row_colors, col_colors), the maximal configuration is:
    # fill exactly the cells where row_color == col_color.
    # This configuration is valid-maximal iff:
    # - every row has at least one matching column of its color
    # - every column has at least one matching row of its color
    #
    # Those conditions are equivalent to:
    #   set of colors present among rows == set of colors present among columns.
    #
    # We count distinct placements with colors (so global color swap counts as distinct).

    def colors_present(bits):
        has_white = any(bits)
        has_black = any(b == 0 for b in bits)
        return (has_white, has_black)

    total = 0
    for row in product((0, 1), repeat=n):
        rw = colors_present(row)
        for col in product((0, 1), repeat=n):
            cw = colors_present(col)
            if rw == cw:
                # Additionally, ensure that each row and column actually
                # has at least one chip (i.e., a matching color exists).
                # Given rw == cw, this reduces to checking:
                # - if a row is white, there exists a white column
                # - if a row is black, there exists a black column
                # and similarly for columns; which is already implied by rw == cw
                # provided we also exclude the impossible case of empty matches.
                #
                # Explicitly check non-emptiness of each row/column under the fill rule:
                ok = True
                # Precompute counts of white/black columns
                cnt_col_white = sum(col)
                cnt_col_black = n - cnt_col_white
                if cnt_col_white == 0 and any(r == 1 for r in row):
                    ok = False
                if cnt_col_black == 0 and any(r == 0 for r in row):
                    ok = False
                # Precompute counts of white/black rows
                cnt_row_white = sum(row)
                cnt_row_black = n - cnt_row_white
                if cnt_row_white == 0 and any(c == 1 for c in col):
                    ok = False
                if cnt_row_black == 0 and any(c == 0 for c in col):
                    ok = False
                if ok:
                    total += 1
    return total

# 调用 solve
result = solve(inputs['size'])
print(result)