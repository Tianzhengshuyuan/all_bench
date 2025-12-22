inputs = {'grid_size': 5}

from itertools import product

def solve(grid_size):
    n = grid_size
    
    # We need to place chips such that:
    # 1. Each cell contains at most one chip
    # 2. All chips in same row have same color
    # 3. All chips in same column have same color
    # 4. Grid is maximal - no additional chip can be placed without violating conditions
    
    # Key insight: Each row can be in one of 3 states: empty (E), white (W), black (B)
    # Each column can be in one of 3 states: empty (E), white (W), black (B)
    # A cell (i,j) has a chip iff row[i] and col[j] are both non-empty AND same color
    
    # Maximality: For each empty cell (i,j), we cannot place any chip.
    # An empty cell occurs when:
    #   - row[i] = E, or
    #   - col[j] = E, or  
    #   - row[i] != col[j] (different colors)
    
    # For an empty cell (i,j), we can place a chip of color c if:
    #   - If row[i] = E: row becomes color c, need col[j] = E or col[j] = c
    #   - If row[i] = c: need col[j] = E or col[j] = c
    #   - If row[i] = other color: cannot place color c
    
    # So for cell (i,j) to be blocked for ALL colors:
    #   - If row[i] = E and col[j] = E: can place any color -> NOT blocked
    #   - If row[i] = E and col[j] = W: can place white -> NOT blocked
    #   - If row[i] = E and col[j] = B: can place black -> NOT blocked
    #   - If row[i] = W and col[j] = E: can place white -> NOT blocked
    #   - If row[i] = B and col[j] = E: can place black -> NOT blocked
    #   - If row[i] = W and col[j] = W: cell has chip (not empty)
    #   - If row[i] = B and col[j] = B: cell has chip (not empty)
    #   - If row[i] = W and col[j] = B: can't place white (col is B), can't place black (row is W) -> BLOCKED
    #   - If row[i] = B and col[j] = W: can't place black (col is W), can't place white (row is B) -> BLOCKED
    
    # So maximality requires: for every (i,j), either there's a chip OR (row[i], col[j]) are opposite colors
    # This means: no row or column can be empty, AND for each (i,j), row[i] == col[j] or they're opposite
    # Since opposite means {W,B}, this is always satisfied when both are non-empty.
    
    # Wait, but we also need to ensure the configuration is valid. Let me reconsider.
    # If row[i] = W and col[j] = B, cell (i,j) is empty and blocked. Good.
    # If row[i] = W and col[j] = W, cell (i,j) has a white chip.
    # If row[i] = E, then for any col[j] != E, we can add a chip. So row[i] = E is not allowed for maximality
    # unless all columns are also E. But if all columns are E, the grid is empty, and we can add a chip.
    
    # So for maximality: no row can be E, no column can be E.
    # With this, every cell (i,j) either has a chip (same color) or is blocked (opposite colors).
    
    # But wait - we're overcounting. Different (row_colors, col_colors) assignments can give the same chip placement.
    # Actually no - the chip placement uniquely determines which cells have chips.
    # But we need to be careful: the "color" of a row/column is determined by the chips in it.
    
    # Let me reconsider the model:
    # - Assign each row a color W or B
    # - Assign each column a color W or B  
    # - Cell (i,j) has a chip iff row[i] == col[j]
    # - This is maximal iff every row has at least one chip AND every column has at least one chip
    
    # For row i with color c to have a chip, there must be some column j with color c.
    # For column j with color c to have a chip, there must be some row i with color c.
    
    # So: if there are w rows with color W, and w' columns with color W,
    # then w > 0 iff w' > 0, and (n-w) > 0 iff (n-w') > 0.
    # This means: w > 0 <=> w' > 0, and w < n <=> w' < n.
    # Cases: (w=0, w'=0), (w=n, w'=n), (0 < w < n and 0 < w' < n)
    
    # But (w=0, w'=0) means all rows B, all columns B -> all cells have chips. Valid.
    # (w=n, w'=n) means all rows W, all columns W -> all cells have chips. Valid.
    # (0 < w < n, 0 < w' < n) -> both colors exist in rows and columns. Valid.
    
    # Invalid: w=0 but w'>0 (no white rows but some white columns -> white columns have no chips)
    # Invalid: w>0 but w'=0, w=n but w'<n, w<n but w'=n
    
    count = 0
    
    for row_colors in product([0, 1], repeat=n):  # 0 = white, 1 = black
        for col_colors in product([0, 1], repeat=n):
            w_rows = sum(1 for c in row_colors if c == 0)
            b_rows = n - w_rows
            w_cols = sum(1 for c in col_colors if c == 0)
            b_cols = n - w_cols
            
            # For white rows to have chips, need w_cols > 0 (if w_rows > 0)
            # For black rows to have chips, need b_cols > 0 (if b_rows > 0)
            # For white cols to have chips, need w_rows > 0 (if w_cols > 0)
            # For black cols to have chips, need b_rows > 0 (if b_cols > 0)
            
            valid = True
            if w_rows > 0 and w_cols == 0:
                valid = False
            if b_rows > 0 and b_cols == 0:
                valid = False
            if w_cols > 0 and w_rows == 0:
                valid = False
            if b_cols > 0 and b_rows == 0:
                valid = False
                
            if valid:
                count += 1
    
    return count

result = solve(5)

# 调用 solve
result = solve(inputs['grid_size'])
print(result)