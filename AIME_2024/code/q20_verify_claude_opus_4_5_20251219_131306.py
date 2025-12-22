inputs = {'grid_size': 5}

from itertools import product

def solve(grid_size):
    n = grid_size
    
    count = 0
    
    # Each row has color 1 (white) or 2 (black)
    # Each column has color 1 (white) or 2 (black)
    # Cell (i,j) has a chip iff row[i] == col[j]
    
    for row_colors in product([1, 2], repeat=n):
        for col_colors in product([1, 2], repeat=n):
            # Check validity: each color used in rows must appear in columns and vice versa
            row_has_white = any(c == 1 for c in row_colors)
            row_has_black = any(c == 2 for c in row_colors)
            col_has_white = any(c == 1 for c in col_colors)
            col_has_black = any(c == 2 for c in col_colors)
            
            # White rows need white columns to have chips
            if row_has_white and not col_has_white:
                continue
            # Black rows need black columns to have chips
            if row_has_black and not col_has_black:
                continue
            # White columns need white rows to have chips
            if col_has_white and not row_has_white:
                continue
            # Black columns need black rows to have chips
            if col_has_black and not row_has_black:
                continue
            
            count += 1
    
    return count

result = solve(5)

# 调用 solve
result = solve(inputs['grid_size'])
print(result)