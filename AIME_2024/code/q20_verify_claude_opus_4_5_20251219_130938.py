inputs = {'grid_size': 5}

from itertools import product

def solve(grid_size):
    n = grid_size
    
    # We need to count valid configurations where:
    # 1. Each cell has at most one chip
    # 2. All chips in same row have same color
    # 3. All chips in same column have same color
    # 4. The configuration is maximal (can't add any more chips)
    
    # For each row, it can be: all white, all black, or empty
    # For each column, it can be: all white, all black, or empty
    # A cell (i,j) has a chip iff row i is non-empty AND column j is non-empty
    # AND the colors match
    
    # Let's denote row colors: 0 = empty, 1 = white, 2 = black
    # Let's denote column colors: 0 = empty, 1 = white, 2 = black
    
    # For a valid configuration:
    # - If row i has color c (c != 0) and column j has color c, then cell (i,j) has a chip of color c
    # - If row i has color c1 and column j has color c2 where c1 != c2 and both != 0, then cell (i,j) is empty
    # - If row i is empty (0), then all cells in row i are empty
    # - If column j is empty (0), then all cells in column j are empty
    
    # Maximality condition:
    # - For each empty cell (i,j), placing a chip there would violate a condition
    # - If row i is empty and column j is empty, we could place any chip there -> invalid
    # - If row i is empty and column j has color c, we could place a chip of color c -> invalid
    #   UNLESS there's another column with a different color that intersects this row
    # - Similarly for empty columns
    
    # Actually, let's think more carefully:
    # If row i is empty, then for maximality, every column must have chips of both colors
    # appearing in different rows, so we can't extend. But a column has only one color!
    # So if row i is empty, for each column j, there must be a conflict preventing placement.
    # If column j has color c, we can place color c in (i,j). To prevent this, 
    # row i must "want" a different color. But row i is empty...
    
    # Let me reconsider: row i being "empty" means no chips in row i.
    # For maximality: for each empty cell (i,j), we cannot place any chip.
    # If we try to place a white chip at (i,j):
    #   - All existing chips in row i must be white (or row i is empty)
    #   - All existing chips in column j must be white (or column j is empty)
    # If we try to place a black chip at (i,j):
    #   - All existing chips in row i must be black (or row i is empty)  
    #   - All existing chips in column j must be black (or column j is empty)
    
    # So cell (i,j) is blocked iff:
    #   - (row i has white AND column j has black) OR (row i has black AND column j has white)
    #   - OR row i has both colors (impossible by constraint)
    #   - OR column j has both colors (impossible by constraint)
    #   - OR cell (i,j) already has a chip
    
    # For an empty cell (i,j) with empty row i and empty column j: we can place any chip -> not maximal
    # For an empty cell (i,j) with empty row i and column j has color c: we can place color c -> not maximal
    # For an empty cell (i,j) with row i has color c and empty column j: we can place color c -> not maximal
    # For an empty cell (i,j) with row i has color c1 and column j has color c2:
    #   - If c1 == c2, cell should have a chip (not empty)
    #   - If c1 != c2, cell is blocked -> OK
    
    # So for maximality:
    # - No row can be empty
    # - No column can be empty
    # - If row i has color c1 and column j has color c2 and c1 == c2, then (i,j) has a chip
    
    # This means: each row has a color (W or B), each column has a color (W or B)
    # Cell (i,j) has a chip iff row_color[i] == col_color[j]
    
    count = 0
    
    # Iterate over all possible row colorings (1=white, 2=black for each row)
    # and column colorings
    for row_colors in product([1, 2], repeat=n):
        for col_colors in product([1, 2], repeat=n):
            # Check that the configuration uses at most 25 white and 25 black chips
            white_count = 0
            black_count = 0
            for i in range(n):
                for j in range(n):
                    if row_colors[i] == col_colors[j]:
                        if row_colors[i] == 1:
                            white_count += 1
                        else:
                            black_count += 1
            
            if white_count <= 25 and black_count <= 25:
                count += 1
    
    return count

result = solve(5)

# 调用 solve
result = solve(inputs['grid_size'])
print(result)