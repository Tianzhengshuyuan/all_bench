inputs = {'grid_size': 5}

from itertools import product

def solve(grid_size):
    n = grid_size
    
    # We need to count valid configurations where:
    # 1. Each cell has at most one chip
    # 2. All chips in same row have same color
    # 3. All chips in same column have same color
    # 4. The configuration is maximal (can't add any more chips)
    
    # Each row can be: empty (0), white (1), or black (2)
    # Each column can be: empty (0), white (1), or black (2)
    # Cell (i,j) has a chip iff row[i] and col[j] are both non-empty AND same color
    
    # For maximality, every empty cell must be blocked for BOTH colors.
    # An empty cell (i,j) can have white placed if:
    #   - row i is empty or white, AND column j is empty or white
    # An empty cell (i,j) can have black placed if:
    #   - row i is empty or black, AND column j is empty or black
    # 
    # Cell is blocked iff it cannot have white AND cannot have black placed.
    
    count = 0
    
    for row_colors in product([0, 1, 2], repeat=n):
        for col_colors in product([0, 1, 2], repeat=n):
            # Build the grid
            grid = [[0]*n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    if row_colors[i] != 0 and col_colors[j] != 0 and row_colors[i] == col_colors[j]:
                        grid[i][j] = row_colors[i]
            
            # Check consistency: row state must match actual chips
            valid = True
            for i in range(n):
                chips_in_row = set(grid[i][j] for j in range(n) if grid[i][j] != 0)
                if row_colors[i] == 0:
                    if chips_in_row:  # row marked empty but has chips
                        valid = False
                        break
                else:
                    if not chips_in_row:  # row marked with color but no chips
                        valid = False
                        break
                    if chips_in_row != {row_colors[i]}:  # wrong color
                        valid = False
                        break
            if not valid:
                continue
            
            for j in range(n):
                chips_in_col = set(grid[i][j] for i in range(n) if grid[i][j] != 0)
                if col_colors[j] == 0:
                    if chips_in_col:
                        valid = False
                        break
                else:
                    if not chips_in_col:
                        valid = False
                        break
                    if chips_in_col != {col_colors[j]}:
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
                        can_white = (row_colors[i] == 0 or row_colors[i] == 1) and \
                                   (col_colors[j] == 0 or col_colors[j] == 1)
                        # Can we place black (2)?
                        can_black = (row_colors[i] == 0 or row_colors[i] == 2) and \
                                   (col_colors[j] == 0 or col_colors[j] == 2)
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