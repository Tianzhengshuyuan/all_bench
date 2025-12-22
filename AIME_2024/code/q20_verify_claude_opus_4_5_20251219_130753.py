inputs = {'grid_size': 5}

def solve(grid_size):
    """
    Solve the chip placement problem on a grid_size x grid_size grid.
    
    Conditions:
    1. Each cell contains at most one chip
    2. All chips in the same row have the same color
    3. All chips in the same column have the same color
    4. Any additional chip would violate conditions 1 or 2 or 3 (maximal configuration)
    
    For maximality, every empty cell must be blocked. An empty cell (i,j) is blocked only if:
    - Row i has chips of color C1 AND column j has chips of color C2 AND C1 != C2
    
    This means no row or column can be empty (otherwise we could add a chip).
    
    Each row has a color (W or B), each column has a color (W or B).
    Cell (i,j) has a chip iff row[i] color == col[j] color.
    
    For validity (every row and column has at least one chip):
    - If there are w white rows and w' white columns:
      - White rows need w' > 0 to have chips (if w > 0)
      - Black rows (n-w) need (n-w') > 0 to have chips (if w < n)
      - Similarly for columns
    
    Valid cases:
    1. w = 0, w' = 0: all black rows, all black columns -> full grid of black chips
    2. w = n, w' = n: all white rows, all white columns -> full grid of white chips
    3. 0 < w < n and 0 < w' < n: mixed case, both colors present in rows and columns
    
    For counting, we need to be careful about what we're counting.
    The problem asks for the number of ways to place chips (configurations).
    
    A configuration is determined by which cells have chips and what color each chip is.
    
    Given row colors and column colors:
    - Cell (i,j) has a chip of color C iff row[i] = C and col[j] = C
    
    Two different (row_colors, col_colors) assignments give the same configuration iff
    they produce the same set of (cell, color) pairs.
    
    If we swap all W<->B in both rows and columns, we get a different configuration
    (white chips become black and vice versa).
    
    So each (row_colors, col_colors) gives a unique configuration.
    
    Count of valid configurations:
    - Case w=0, w'=0: C(n,0)*C(n,0) = 1
    - Case w=n, w'=n: C(n,n)*C(n,n) = 1
    - Case 0<w<n, 0<w'<n: sum over w=1..n-1, w'=1..n-1 of C(n,w)*C(n,w')
    
    But we also need w=0 with any w' where black rows still have chips.
    If w=0 (all rows black), we need b' = n-w' > 0, i.e., w' < n.
    If w'=n (all cols white), black rows have no chips -> invalid.
    So w=0 requires w' < n, and for cols to have chips, w' > 0 requires w > 0.
    So w=0 requires w'=0.
    
    Similarly w=n requires w'=n.
    
    Total = 1 + 1 + sum_{w=1}^{n-1} sum_{w'=1}^{n-1} C(n,w)*C(n,w')
          = 2 + (2^n - 2)^2
    
    For n=5: 2 + (32-2)^2 = 2 + 900 = 902
    
    But this doesn't match expected. Let me reconsider the problem.
    
    Re-reading: "some of these chips" - we place chips, and the configuration must be maximal.
    
    Actually, I think empty rows/columns might be allowed in certain cases.
    Let me reconsider maximality more carefully.
    
    For an empty cell (i,j), we can add a chip of color C if:
    - Row i is empty OR has color C
    - Column j is empty OR has color C
    
    So cell (i,j) is blocked iff for BOTH colors, at least one of row/col has the opposite color.
    - Blocked for white: row has black OR col has black
    - Blocked for black: row has white OR col has white
    - Blocked for both: (row=B or col=B) AND (row=W or col=W)
    
    This requires row and col to have opposite colors (both non-empty with different colors).
    
    So empty rows/cols are NOT allowed for maximality (we could add chips there).
    
    My analysis gives 902 for n=5. Let me check if the answer format expects something else.
    """
    from math import comb
    
    n = grid_size
    
    # Case 1: all rows same color, all cols same color (must match)
    # w=0,w'=0 (all black) or w=n,w'=n (all white): 2 configurations
    count = 2
    
    # Case 2: mixed - 0 < w < n and 0 < w' < n
    # For each such (w, w'), we choose which rows are white and which cols are white
    for w in range(1, n):
        for wp in range(1, n):
            count += comb(n, w) * comb(n, wp)
    
    return count


result = solve(5)

# 调用 solve
result = solve(inputs['grid_size'])
print(result)