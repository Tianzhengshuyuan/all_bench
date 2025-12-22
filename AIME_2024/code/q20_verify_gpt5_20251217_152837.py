inputs = {'size': 5}

def solve(size: int) -> int:
    n = size
    if n <= 0:
        return 1

    total = 0
    from itertools import product

    for rows in product((0, 1), repeat=n):
        has_white_row = any(rows)
        has_black_row = any(r == 0 for r in rows)
        for cols in product((0, 1), repeat=n):
            has_white_col = any(cols)
            has_black_col = any(c == 0 for c in cols)

            if (has_white_row != has_white_col) or (has_black_row != has_black_col):
                continue

            cnt_col_white = sum(cols)
            cnt_col_black = n - cnt_col_white
            if any((r == 1 and cnt_col_white == 0) or (r == 0 and cnt_col_black == 0) for r in rows):
                continue

            cnt_row_white = sum(rows)
            cnt_row_black = n - cnt_row_white
            if any((c == 1 and cnt_row_white == 0) or (c == 0 and cnt_row_black == 0) for c in cols):
                continue

            total += 1

    return total

# 调用 solve
result = solve(inputs['size'])
print(result)