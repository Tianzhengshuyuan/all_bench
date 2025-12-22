inputs = {'grid_size': 5}

from itertools import product

def solve(grid_size):
    n = grid_size
    
    # We need to count valid configurations where:
    # 1. Each cell has at most one chip
    # 2. All chips in same row have same color, all chips in same column have same color
    # 3. Configuration is maximal (can't add any more chips without violating rules)
    
    # For each row, it's either: empty, all white chips, or all black chips
    # For each column, it's either: empty, all white chips, or all black chips
    # A cell (i,j) has a chip iff row i is non-empty AND column j is non-empty AND they have same color
    
    # Let's enumerate: for each row, state in {0: empty, 1: white, 2: black}
    # For each column, state in {0: empty, 1: white, 2: black}
    
    count = 0
    
    # Enumerate all possible row states and column states
    for row_states in product(range(3), repeat=n):
        for col_states in product(range(3), repeat=n):
            # Build the grid based on row and column states
            # Cell (i,j) has a chip iff row_states[i] != 0 and col_states[j] != 0 and row_states[i] == col_states[j]
            
            # Check maximality: for every empty cell, we cannot add a chip
            valid = True
            
            for i in range(n):
                if not valid:
                    break
                for j in range(n):
                    # Check if cell (i,j) is empty
                    has_chip = (row_states[i] != 0 and col_states[j] != 0 and row_states[i] == col_states[j])
                    
                    if not has_chip:
                        # Cell is empty. Check if we can add a chip here.
                        # We can add a chip of color c if:
                        # - All existing chips in row i have color c (or row i is empty)
                        # - All existing chips in column j have color c (or column j is empty)
                        
                        # What color does row i have? (based on existing chips)
                        row_color = None  # None means no chips in this row yet
                        for jj in range(n):
                            cell_has_chip = (row_states[i] != 0 and col_states[jj] != 0 and row_states[i] == col_states[jj])
                            if cell_has_chip:
                                row_color = row_states[i]
                                break
                        
                        # What color does column j have?
                        col_color = None
                        for ii in range(n):
                            cell_has_chip = (row_states[ii] != 0 and col_states[j] != 0 and row_states[ii] == col_states[j])
                            if cell_has_chip:
                                col_color = col_states[j]
                                break
                        
                        # Can we add white chip (color 1)?
                        can_add_white = (row_color is None or row_color == 1) and (col_color is None or col_color == 1)
                        
                        # Can we add black chip (color 2)?
                        can_add_black = (row_color is None or row_color == 2) and (col_color is None or col_color == 2)
                        
                        if can_add_white or can_add_black:
                            valid = False
                            break
            
            if valid:
                count += 1
    
    return count

result = solve(5)

# 调用 solve
result = solve(inputs['grid_size'])
print(result)