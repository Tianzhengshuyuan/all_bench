inputs = {'grid_size': 5}

def solve(grid_size):
    from itertools import product
    
    n = grid_size
    count = 0
    
    # Each row has color 1 (white) or 2 (black)
    # Each column has color 1 (white) or 2 (black)
    # Cell (i,j) has a chip iff row[i] == col[j]
    
    for row_colors in product([1, 2], repeat=n):
        for col_colors in product([1, 2], repeat=n):
            # For validity: each row must have at least one chip
            # Row i (color c) has chip iff some column j has color c
            valid = True
            
            # Count colors in rows and columns
            white_rows = sum(1 for c in row_colors if c == 1)
            black_rows = n - white_rows
            white_cols = sum(1 for c in col_colors if c == 1)
            black_cols = n - white_cols
            
            # White rows need white columns to have chips
            if white_rows > 0 and white_cols == 0:
                valid = False
            # Black rows need black columns to have chips
            if black_rows > 0 and black_cols == 0:
                valid = False
            # White columns need white rows to have chips
            if white_cols > 0 and white_rows == 0:
                valid = False
            # Black columns need black rows to have chips
            if black_cols > 0 and black_rows == 0:
                valid = False
            
            # For maximality: every empty cell must be blocked
            # Empty cell (i,j) where row[i] != col[j] is blocked iff both colors exist
            # This requires both white and black to exist in rows AND columns
            # OR all cells are filled (all same color)
            
            if valid:
                # Check if all cells filled (all rows and cols same color)
                all_same = (white_rows == n and white_cols == n) or (black_rows == n and black_cols == n)
                # Or mixed case where both colors exist
                mixed = (white_rows > 0 and black_rows > 0 and white_cols > 0 and black_cols > 0)
                
                if all_same or mixed:
                    count += 1
    
    return count

result = solve(5)

# 调用 solve
result = solve(inputs['grid_size'])
print(result)