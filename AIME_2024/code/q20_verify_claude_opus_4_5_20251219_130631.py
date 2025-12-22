inputs = {'grid_size': 5}

def solve(grid_size):
    n = grid_size
    
    # We need to place chips such that:
    # 1. Each cell contains at most one chip
    # 2. All chips in same row have same color
    # 3. All chips in same column have same color
    # 4. Grid is maximal - no additional chip can be placed without violating conditions
    
    # Key insight: The problem counts chip PLACEMENTS (which cells have chips), 
    # not colorings. Two different colorings giving the same occupied cells count as one.
    
    # Let's think about what configurations are possible:
    # - Each row can be: empty, or have some chips (all same color)
    # - Each column can be: empty, or have some chips (all same color)
    # - A cell has a chip iff its row and column both have chips AND same color
    
    # For maximality, we need that no chip can be added anywhere.
    # 
    # Let R_W = rows with white chips, R_B = rows with black chips, R_E = empty rows
    # Let C_W = cols with white chips, C_B = cols with black chips, C_E = empty cols
    
    # For an empty cell (i,j) to be blocked:
    # - If i in R_W, j in C_B: blocked (colors conflict)
    # - If i in R_B, j in C_W: blocked (colors conflict)
    # - If i in R_E, j in C_W: can add white -> NOT blocked
    # - If i in R_E, j in C_B: can add black -> NOT blocked
    # - If i in R_W, j in C_E: can add white -> NOT blocked
    # - If i in R_B, j in C_E: can add black -> NOT blocked
    # - If i in R_E, j in C_E: can add any color -> NOT blocked
    
    # So for maximality:
    # - If R_E is non-empty, then C_E must be empty AND C_W must be empty AND C_B must be empty
    #   But that means no columns have chips, so no chips at all, but then we can add chips. Contradiction.
    # - So R_E must be empty (all rows have chips)
    # - Similarly C_E must be empty (all columns have chips)
    
    # With R_E = C_E = empty:
    # - Every row is either W or B
    # - Every column is either W or B
    # - Cell (i,j) has chip iff row[i] color == col[j] color
    # - For row i (color c) to have a chip, need some column with color c
    # - For column j (color c) to have a chip, need some row with color c
    
    # Let w = |R_W|, b = |R_B| = n - w
    # Let w' = |C_W|, b' = |C_B| = n - w'
    
    # Validity conditions:
    # - If w > 0, need w' > 0 (white rows need white columns)
    # - If b > 0, need b' > 0 (black rows need black columns)
    # - If w' > 0, need w > 0 (white columns need white rows)
    # - If b' > 0, need b > 0 (black columns need black rows)
    
    # This means: (w > 0 iff w' > 0) and (b > 0 iff b' > 0)
    # Since w + b = n and w' + b' = n:
    # Valid cases: (w=0, w'=0), (w=n, w'=n), or (0 < w < n and 0 < w' < n)
    
    # Now count distinct chip patterns:
    # The chip pattern is the set of occupied cells.
    # For (row_colors, col_colors), occupied = {(i,j) : row[i] == col[j]}
    
    # Two colorings give same pattern iff one is obtained from other by swapping W<->B globally.
    # 
    # Case 1: w=0, w'=0 (all rows B, all cols B) -> all cells occupied
    # Case 2: w=n, w'=n (all rows W, all cols W) -> all cells occupied (same pattern as Case 1)
    # So Cases 1 and 2 together give 1 distinct pattern.
    
    # Case 3: 0 < w < n and 0 < w' < n
    # Number of (row_colors, col_colors) pairs: sum over w=1..n-1, w'=1..n-1 of C(n,w)*C(n,w')
    # = (2^n - 2)^2
    # 
    # Each pattern is counted exactly twice (original and color-swapped).
    # So number of distinct patterns = (2^n - 2)^2 / 2
    
    # Total = 1 + (2^n - 2)^2 / 2
    
    # For n=5: 1 + (32-2)^2 / 2 = 1 + 900/2 = 1 + 450 = 451
    
    # But the answer hint says we should do casework on columns. Let me reconsider.
    # Maybe empty rows/columns ARE allowed in some cases?
    
    # Re-reading the problem: "any additional chip placed on the grid would violate one or more of the previous two conditions"
    # Condition 1: each cell contains at most one chip
    # Condition 2: all chips in same row have same color, all chips in same column have same color
    
    # If we try to add a chip to an empty cell, condition 1 is satisfied.
    # Condition 2 is violated if the new chip's color conflicts with existing chips in its row or column.
    
    # So for an empty cell (i,j), adding color c is blocked if:
    # - Row i has chips of color != c, OR
    # - Column j has chips of color != c
    
    # For cell to be blocked for ALL colors:
    # - Row i has chips (some color c1) AND column j has chips (some color c2) AND c1 != c2
    
    # If row i is empty: we can add any color (row becomes that color, check column)
    #   - If column j is empty: can add any color -> NOT blocked
    #   - If column j has color c: can add color c -> NOT blocked
    # So if row i is empty, cell (i,j) is never blocked. Same for empty column.
    
    # For maximality: no empty rows, no empty columns.
    
    # Hmm, my analysis seems correct. Let me reconsider what we're counting.
    
    # Wait - the problem says "indistinguishable white chips and indistinguishable black chips".
    # This means we're counting placements where we specify which cells have which color chip.
    # Two placements are different if they differ in which cells have chips OR in the colors.
    
    # So we're counting (occupied cells, coloring) pairs, not just occupied cells!
    
    # With this interpretation:
    # - All rows/cols must be non-empty for maximality
    # - Each row is W or B, each column is W or B
    # - Valid iff (w>0 => w'>0) and (b>0 => b'>0) and (w'>0 => w>0) and (b'>0 => b>0)
    
    # Count: 2 (all same color) + (2^n - 2)^2 (mixed)
    # = 2 + (2^5 - 2)^2 = 2 + 30^2 = 2 + 900 = 902
    
    from math import comb
    
    # All same color: 2 configurations (all white or all black)
    # Mixed: for each w in 1..n-1 and w' in 1..n-1, choose which rows are white and which cols are white
    
    count = 2  # all white, all black
    
    for w in range(1, n):
        for wp in range(1, n):
            count += comb(n, w) * comb(n, wp)
    
    return count

result = solve(5)

# 调用 solve
result = solve(inputs['grid_size'])
print(result)