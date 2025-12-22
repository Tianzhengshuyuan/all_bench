inputs = {'grid_size': 5}

from itertools import product

def solve(grid_size):
    n = grid_size
    
    # We need to count valid configurations where:
    # 1. Each cell has at most one chip
    # 2. All chips in same row have same color
    # 3. All chips in same column have same color
    # 4. The configuration is maximal (can't add any more chips without violating rules)
    
    # For each row, we can assign: 'W' (white), 'B' (black), or 'E' (empty/no chips)
    # For each column, we can assign: 'W', 'B', or 'E'
    
    # A cell (i,j) has a chip if and only if:
    # - row i is not 'E' and column j is not 'E'
    # - row i color == column j color
    
    # For maximality:
    # - If row i is 'E', then for every column j that is not 'E', 
    #   there must be some row with the opposite color that intersects column j
    #   (otherwise we could add a chip at (i,j) with column j's color)
    # - Similarly for columns
    
    count = 0
    
    # Iterate over all possible row and column assignments
    # 0 = Empty, 1 = White, 2 = Black
    for row_assign in product([0, 1, 2], repeat=n):
        for col_assign in product([0, 1, 2], repeat=n):
            # Check maximality condition
            valid = True
            
            # For each empty row
            for i in range(n):
                if row_assign[i] == 0:  # row i is empty
                    # For each non-empty column j
                    for j in range(n):
                        if col_assign[j] != 0:  # column j has a color
                            # Check if we can add a chip at (i, j) with color col_assign[j]
                            # We can add it unless there's already a chip there or it violates rules
                            # Since row i is empty, adding a chip with col_assign[j] color is possible
                            # unless... we need to check if this would be blocked
                            # Actually, if row i is empty and col j has color c,
                            # we could place a chip of color c at (i,j) and assign row i color c
                            # This violates maximality unless... 
                            # Wait, the row being empty means no chips in that row
                            # If we add a chip at (i,j), row i would have color c
                            # This is always possible, so maximality is violated
                            valid = False
                            break
                    if not valid:
                        break
            
            if not valid:
                continue
                
            # For each empty column
            for j in range(n):
                if col_assign[j] == 0:  # column j is empty
                    for i in range(n):
                        if row_assign[i] != 0:  # row i has a color
                            valid = False
                            break
                    if not valid:
                        break
            
            if not valid:
                continue
            
            # Now check: for each cell (i,j) that is empty (no chip),
            # can we add a chip there?
            # Cell (i,j) has a chip iff row_assign[i] == col_assign[j] and both != 0
            
            for i in range(n):
                if not valid:
                    break
                for j in range(n):
                    has_chip = (row_assign[i] != 0 and col_assign[j] != 0 and row_assign[i] == col_assign[j])
                    if not has_chip:
                        # Can we add a chip here?
                        # If row i is empty or col j is empty, we already handled above
                        # If both have colors but different, we cannot add (would violate same-color rule)
                        # If both have same color, there's already a chip (contradiction)
                        if row_assign[i] != 0 and col_assign[j] != 0:
                            # Different colors, can't add - this is fine
                            pass
                        else:
                            # One or both empty - but we already checked this case above
                            pass
            
            if valid:
                count += 1
    
    # The above counts configurations where no row or column is empty
    # and each cell either has matching colors (chip) or different colors (no chip)
    # But we need to reconsider...
    
    # Let me reconsider: we need both row and column to be non-empty for maximality
    # So we only consider assignments where all rows and columns have a color (W or B)
    
    count = 0
    for row_assign in product([1, 2], repeat=n):  # 1=White, 2=Black
        for col_assign in product([1, 2], repeat=n):
            # A chip is at (i,j) iff row_assign[i] == col_assign[j]
            # Check maximality: for each empty cell, we cannot add a chip
            # Empty cell means row_assign[i] != col_assign[j]
            # Adding a chip would require same color, which would change row or column color
            # But row/column colors are fixed by existing chips
            # So if row i has white chips and col j has black chips, we can't add at (i,j)
            # This is automatically satisfied
            
            # But we also need at least one chip in each row and column
            # Row i has chips in columns j where col_assign[j] == row_assign[i]
            # Column j has chips in rows i where row_assign[i] == col_assign[j]
            
            # Check each row has at least one chip
            valid = True
            for i in range(n):
                has_chip_in_row = any(col_assign[j] == row_assign[i] for j in range(n))
                if not has_chip_in_row:
                    valid = False
                    break
            
            if not valid:
                continue
                
            # Check each column has at least one chip
            for j in range(n):
                has_chip_in_col = any(row_assign[i] == col_assign[j] for i in range(n))
                if not has_chip_in_col:
                    valid = False
                    break
            
            if valid:
                count += 1
    
    return count

result = solve(5)

# 调用 solve
result = solve(inputs['grid_size'])
print(result)