inputs = {'grid_size': 5}

def solve(grid_size):
    n = grid_size
    
    # We'll enumerate all possible chip placements and check validity + maximality
    # A placement is defined by: for each cell, it's empty (0), white (1), or black (2)
    # But this is 3^25 which is too large.
    
    # Better approach: think in terms of row/column color assignments
    # Each row: 0 (no constraint yet), 1 (white), 2 (black)
    # Each column: 0 (no constraint yet), 1 (white), 2 (black)
    # A chip exists at (i,j) with color c iff row[i]=c and col[j]=c (both non-zero, same)
    
    # For maximality: for every empty cell (i,j), we cannot place white AND cannot place black
    # Can place white at (i,j): (row[i] in {0,1}) and (col[j] in {0,1})
    # Can place black at (i,j): (row[i] in {0,2}) and (col[j] in {0,2})
    # Blocked for both: NOT(can_white) AND NOT(can_black)
    # = (row[i]=2 or col[j]=2) AND (row[i]=1 or col[j]=1)
    
    # This means: {row[i], col[j]} must contain both 1 and 2
    # So for empty cells, we need row and col to have opposite non-zero colors
    
    # For cells with chips: row[i] = col[j] (both 1 or both 2)
    
    # Consistency: if row[i] != 0, there must be at least one chip in row i
    # This means: exists j such that col[j] = row[i]
    
    from itertools import product
    
    count = 0
    
    for row_colors in product([0, 1, 2], repeat=n):
        for col_colors in product([0, 1, 2], repeat=n):
            # Check consistency: non-zero row must have matching column and vice versa
            valid = True
            
            for i in range(n):
                if row_colors[i] != 0:
                    if not any(col_colors[j] == row_colors[i] for j in range(n)):
                        valid = False
                        break
            if not valid:
                continue
                
            for j in range(n):
                if col_colors[j] != 0:
                    if not any(row_colors[i] == col_colors[j] for i in range(n)):
                        valid = False
                        break
            if not valid:
                continue
            
            # Check maximality: every empty cell must be blocked for both colors
            maximal = True
            for i in range(n):
                for j in range(n):
                    # Cell has chip if both non-zero and equal
                    has_chip = (row_colors[i] != 0 and col_colors[j] != 0 and 
                               row_colors[i] == col_colors[j])
                    if not has_chip:
                        # Must be blocked for both colors
                        # Blocked = {row[i], col[j]} contains both 1 and 2
                        colors_present = {row_colors[i], col_colors[j]} - {0}
                        if len(colors_present) < 2:
                            maximal = False
                            break
                if not maximal:
                    break
            
            if maximal:
                count += 1
    
    return count

result = solve(5)

# 调用 solve
result = solve(inputs['grid_size'])
print(result)