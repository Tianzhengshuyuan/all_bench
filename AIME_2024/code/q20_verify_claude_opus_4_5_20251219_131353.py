inputs = {'grid_size': 5}

def solve(grid_size):
    n = grid_size
    
    # We enumerate all possible ways to assign:
    # - Each row: white (W), black (B), or no chips (but constrained by maximality)
    # - Each column: white (W), black (B), or no chips
    # 
    # For maximality, every empty cell (i,j) must be blocked.
    # Cell is blocked iff we can't place white AND can't place black.
    # Can place white: row allows white (empty or white) AND col allows white (empty or white)
    # Can place black: row allows black (empty or black) AND col allows black (empty or black)
    # 
    # Blocked = NOT(can_white) AND NOT(can_black)
    # = (row=B or col=B) AND (row=W or col=W)
    # This requires {row, col} to contain both W and B (both must be non-empty with different colors)
    
    # So for every empty cell, row and column must have opposite non-empty colors.
    # This means: if any row is empty, we can find an empty cell that's not blocked.
    # Unless... all columns are also empty. But then the whole grid is empty and we can add chips.
    
    # Therefore: all rows must be W or B, all columns must be W or B.
    # Additionally, for a row to actually have chips (and thus "be" that color),
    # there must be at least one column of the same color.
    
    from itertools import product
    
    count = 0
    
    for row_colors in product([1, 2], repeat=n):  # 1=white, 2=black
        for col_colors in product([1, 2], repeat=n):
            # Check that each row has at least one chip (matching column exists)
            # and each column has at least one chip (matching row exists)
            
            white_rows = sum(1 for c in row_colors if c == 1)
            black_rows = n - white_rows
            white_cols = sum(1 for c in col_colors if c == 1)
            black_cols = n - white_cols
            
            # White rows need white columns, black rows need black columns
            # White columns need white rows, black columns need black rows
            valid = True
            if white_rows > 0 and white_cols == 0:
                valid = False
            if black_rows > 0 and black_cols == 0:
                valid = False
            if white_cols > 0 and white_rows == 0:
                valid = False
            if black_cols > 0 and black_rows == 0:
                valid = False
            
            if valid:
                count += 1
    
    return count

result = solve(5)

# 调用 solve
result = solve(inputs['grid_size'])
print(result)