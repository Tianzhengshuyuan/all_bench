inputs = {'grid_size': 5}

def solve(grid_size):
    from itertools import product
    
    n = grid_size
    count = 0
    
    # Each row state: 0=empty, 1=white, 2=black
    # Each col state: 0=empty, 1=white, 2=black
    
    for row_states in product([0, 1, 2], repeat=n):
        for col_states in product([0, 1, 2], repeat=n):
            # Build the grid: cell (i,j) has chip if row and col are same non-zero color
            grid = [[0]*n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    if row_states[i] != 0 and col_states[j] != 0 and row_states[i] == col_states[j]:
                        grid[i][j] = row_states[i]
            
            # Check consistency: row state must match actual chips in that row
            valid = True
            for i in range(n):
                chips_in_row = [grid[i][j] for j in range(n) if grid[i][j] != 0]
                if row_states[i] == 0:
                    if chips_in_row:  # row marked empty but has chips
                        valid = False
                        break
                else:
                    if not chips_in_row:  # row marked with color but no chips
                        valid = False
                        break
            if not valid:
                continue
                
            for j in range(n):
                chips_in_col = [grid[i][j] for i in range(n) if grid[i][j] != 0]
                if col_states[j] == 0:
                    if chips_in_col:
                        valid = False
                        break
                else:
                    if not chips_in_col:
                        valid = False
                        break
            if not valid:
                continue
            
            # Check maximality: every empty cell must be blocked for both colors
            maximal = True
            for i in range(n):
                for j in range(n):
                    if grid[i][j] == 0:  # empty cell
                        # Can we place white (1)?
                        can_white = (row_states[i] == 0 or row_states[i] == 1) and \
                                   (col_states[j] == 0 or col_states[j] == 1)
                        # Can we place black (2)?
                        can_black = (row_states[i] == 0 or row_states[i] == 2) and \
                                   (col_states[j] == 0 or col_states[j] == 2)
                        if can_white or can_black:
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