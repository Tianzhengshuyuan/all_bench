inputs = {'grid_size': 5}

def solve(grid_size):
    from itertools import product
    
    n = grid_size
    
    # Each row has color 1 (white) or 2 (black)
    # Each column has color 1 (white) or 2 (black)
    # Cell (i,j) has a chip iff row[i] == col[j]
    
    # For validity: each row/column must have at least one chip
    # This means: if there are white rows, there must be white columns (and vice versa)
    
    # Count distinct CHIP PLACEMENTS (not colorings)
    # Two colorings give same placement iff one is color-swap of other
    
    seen_patterns = set()
    
    for row_colors in product([1, 2], repeat=n):
        for col_colors in product([1, 2], repeat=n):
            # Check validity
            white_rows = sum(1 for c in row_colors if c == 1)
            black_rows = n - white_rows
            white_cols = sum(1 for c in col_colors if c == 1)
            black_cols = n - white_cols
            
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
                # Create the chip pattern (which cells have chips, and what color)
                pattern = []
                for i in range(n):
                    for j in range(n):
                        if row_colors[i] == col_colors[j]:
                            pattern.append((i, j, row_colors[i]))
                        else:
                            pattern.append((i, j, 0))
                
                seen_patterns.add(tuple(pattern))
    
    return len(seen_patterns)

result = solve(5)

# 调用 solve
result = solve(inputs['grid_size'])
print(result)