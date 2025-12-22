inputs = {'grid_size': 5}

def solve(grid_size):
    from itertools import product
    
    n = grid_size
    count = 0
    
    # Each row state: 0=empty, 1=white, 2=black
    # Each col state: 0=empty, 1=white, 2=black
    
    for row_states in product([0, 1, 2], repeat=n):
        for col_states in product([0, 1, 2], repeat=n):
            # Check validity: each non-empty row/col must have at least one chip
            valid = True
            
            # For non-empty row i (color c), need at least one column with color c
            for i in range(n):
                if row_states[i] != 0:
                    if not any(col_states[j] == row_states[i] for j in range(n)):
                        valid = False
                        break
            if not valid:
                continue
                
            # For non-empty col j (color c), need at least one row with color c
            for j in range(n):
                if col_states[j] != 0:
                    if not any(row_states[i] == col_states[j] for i in range(n)):
                        valid = False
                        break
            if not valid:
                continue
            
            # Check maximality: every empty cell must be blocked for both colors
            maximal = True
            for i in range(n):
                for j in range(n):
                    # Cell has chip if both non-empty and same color
                    has_chip = (row_states[i] != 0 and col_states[j] != 0 and 
                               row_states[i] == col_states[j])
                    if not has_chip:
                        # Check if blocked for white (1)
                        blocked_white = (row_states[i] == 2 or col_states[j] == 2)
                        # Check if blocked for black (2)
                        blocked_black = (row_states[i] == 1 or col_states[j] == 1)
                        if not (blocked_white and blocked_black):
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