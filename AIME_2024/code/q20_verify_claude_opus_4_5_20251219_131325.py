inputs = {'grid_size': 5}

from itertools import product

def solve(grid_size):
    n = grid_size
    
    count = 0
    
    # Each row: 0=empty, 1=white, 2=black
    # Each column: 0=empty, 1=white, 2=black
    # Cell (i,j) has chip iff row[i] != 0 and col[j] != 0 and row[i] == col[j]
    
    for row_colors in product([0, 1, 2], repeat=n):
        for col_colors in product([0, 1, 2], repeat=n):
            # Check maximality: every empty cell must be blocked for both colors
            maximal = True
            
            for i in range(n):
                for j in range(n):
                    has_chip = (row_colors[i] != 0 and col_colors[j] != 0 and 
                               row_colors[i] == col_colors[j])
                    if not has_chip:
                        # Check if blocked for white: row is black OR col is black
                        blocked_white = (row_colors[i] == 2 or col_colors[j] == 2)
                        # Check if blocked for black: row is white OR col is white
                        blocked_black = (row_colors[i] == 1 or col_colors[j] == 1)
                        if not (blocked_white and blocked_black):
                            maximal = False
                            break
                if not maximal:
                    break
            
            if not maximal:
                continue
            
            # Check consistency: non-empty row must have at least one chip
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
            
            count += 1
    
    return count

result = solve(5)

# 调用 solve
result = solve(inputs['grid_size'])
print(result)