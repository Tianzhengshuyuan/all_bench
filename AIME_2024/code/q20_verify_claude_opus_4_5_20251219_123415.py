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
    
    # Maximality condition:
    # - For an empty row i: for every color c in {white, black}, there exists a non-empty column j 
    #   with the opposite color (so we can't fill row i with color c)
    # - For an empty column j: for every color c, there exists a non-empty row i with opposite color
    # - For a non-empty row i with color c: every column is either empty or has color c
    #   (otherwise there would be a conflict)
    # - For a non-empty column j with color c: every row is either empty or has color c
    
    # Actually, let's think more carefully:
    # If row i has color c (non-empty), then for cell (i,j) to have a chip, column j must have color c
    # If column j has color c, then for cell (i,j) to have a chip, row i must have color c
    
    # Consistency: if row i has color c1 and column j has color c2:
    # - if c1 != 0 and c2 != 0 and c1 != c2, then cell (i,j) is empty
    # - if c1 != 0 and c2 != 0 and c1 == c2, then cell (i,j) has a chip of color c1
    # - if c1 == 0 or c2 == 0, then cell (i,j) is empty
    
    # Maximality:
    # - Empty row i: we cannot assign any color to it. For color c, there must be some column with opposite color.
    #   So both colors must appear in columns.
    # - Empty column j: both colors must appear in rows.
    # - Non-empty row i with color c: we cannot add more chips. All columns are either empty or same color c.
    #   For each empty column j, we cannot assign color c to it (otherwise we could add chip at (i,j)).
    #   So for empty column j, there must be a row with opposite color of c.
    # - Similarly for non-empty columns.
    
    count = 0
    
    # Enumerate all possible row states and column states
    for row_states in product(range(3), repeat=n):
        for col_states in product(range(3), repeat=n):
            # Check maximality
            valid = True
            
            # For each empty row
            for i in range(n):
                if row_states[i] == 0:
                    # Cannot add white: need some column with black
                    # Cannot add black: need some column with white
                    has_white_col = any(col_states[j] == 1 for j in range(n))
                    has_black_col = any(col_states[j] == 2 for j in range(n))
                    if not (has_white_col and has_black_col):
                        valid = False
                        break
            
            if not valid:
                continue
            
            # For each empty column
            for j in range(n):
                if col_states[j] == 0:
                    has_white_row = any(row_states[i] == 1 for i in range(n))
                    has_black_row = any(row_states[i] == 2 for i in range(n))
                    if not (has_white_row and has_black_row):
                        valid = False
                        break
            
            if not valid:
                continue
            
            # For each non-empty row with color c
            for i in range(n):
                if row_states[i] != 0:
                    c = row_states[i]
                    # All non-empty columns must have same color c
                    for j in range(n):
                        if col_states[j] != 0 and col_states[j] != c:
                            # This is fine, cell (i,j) is empty
                            pass
                    # For each empty column j, we cannot assign color c
                    # So there must be a row with opposite color
                    opp = 3 - c  # if c=1, opp=2; if c=2, opp=1
                    for j in range(n):
                        if col_states[j] == 0:
                            # Need a row with opposite color
                            has_opp_row = any(row_states[ii] == opp for ii in range(n))
                            if not has_opp_row:
                                valid = False
                                break
                    if not valid:
                        break
            
            if not valid:
                continue
            
            # For each non-empty column with color c
            for j in range(n):
                if col_states[j] != 0:
                    c = col_states[j]
                    opp = 3 - c
                    for i in range(n):
                        if row_states[i] == 0:
                            has_opp_col = any(col_states[jj] == opp for jj in range(n))
                            if not has_opp_col:
                                valid = False
                                break
                    if not valid:
                        break
            
            if valid:
                count += 1
    
    return count

result = solve(5)

# 调用 solve
result = solve(inputs['grid_size'])
print(result)