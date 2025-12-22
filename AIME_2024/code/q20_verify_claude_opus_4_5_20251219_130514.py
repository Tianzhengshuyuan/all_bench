inputs = {'grid_size': 5}

from itertools import combinations

def solve(grid_size):
    n = grid_size
    
    # We need to count valid maximal chip placements.
    # Key insight: Each row with chips has a single color, each column with chips has a single color.
    # A cell (i,j) has a chip iff row i has chips AND column j has chips AND they have the same color.
    
    # For maximality: we cannot add any chip to any empty cell.
    # An empty cell (i,j) can receive a chip of color c if:
    #   - Row i is empty or has color c
    #   - Column j is empty or has color c
    # So an empty cell is blocked iff for every color c, either row has opposite color or column has opposite color.
    
    # Let's denote:
    # - W_r = set of rows with white chips
    # - B_r = set of rows with black chips  
    # - E_r = set of empty rows
    # - W_c = set of columns with white chips
    # - B_c = set of columns with black chips
    # - E_c = set of empty columns
    
    # Cell (i,j) has a chip iff (i in W_r and j in W_c) or (i in B_r and j in B_c)
    
    # For maximality, consider empty cell (i,j):
    # Case 1: i in W_r, j in B_c -> blocked (can't place white due to col, can't place black due to row)
    # Case 2: i in B_r, j in W_c -> blocked
    # Case 3: i in W_r, j in E_c -> can place white -> NOT maximal unless no such cell
    # Case 4: i in B_r, j in E_c -> can place black -> NOT maximal
    # Case 5: i in E_r, j in W_c -> can place white -> NOT maximal
    # Case 6: i in E_r, j in B_c -> can place black -> NOT maximal
    # Case 7: i in E_r, j in E_c -> can place any color -> NOT maximal
    
    # So for maximality:
    # - If there's any empty row, all columns must be non-empty AND for each empty row i and each column j,
    #   we need the column to block both colors. But a single column can only be one color, so it can't block both.
    #   Unless... there are no empty rows at all, or no empty columns at all.
    
    # Actually, for an empty row i and column j with color c, we can place color c. So blocked only if no such column.
    # For empty row i to be blocked: every column must be non-empty, and... we still can place the column's color.
    # So empty rows are only allowed if there are no columns at all? That means empty grid, but then we can add chips.
    
    # Conclusion: For maximality, there can be no empty rows and no empty columns.
    # Every row must have at least one chip, every column must have at least one chip.
    
    # With no empty rows/columns:
    # - Each row is either white or black
    # - Each column is either white or black
    # - Cell (i,j) has chip iff row[i] color == col[j] color
    # - Every row has a chip: row i with color c needs at least one column with color c
    # - Every column has a chip: column j with color c needs at least one row with color c
    
    # Let w = number of white rows, b = n - w = number of black rows
    # Let w' = number of white columns, b' = n - w' = number of black columns
    
    # For all white rows to have chips: w' >= 1 (if w >= 1)
    # For all black rows to have chips: b' >= 1 (if b >= 1)
    # For all white columns to have chips: w >= 1 (if w' >= 1)
    # For all black columns to have chips: b >= 1 (if b' >= 1)
    
    # This means: (w = 0 iff w' = 0) and (b = 0 iff b' = 0)
    # Since w + b = n and w' + b' = n:
    # - w = 0 means b = n, and w' = 0 means b' = n. So all black.
    # - w = n means b = 0, and w' = n means b' = 0. So all white.
    # - 0 < w < n means 0 < b < n, and we need 0 < w' < n and 0 < b' < n.
    
    # Valid cases:
    # 1. w = 0, w' = 0 (all black): C(n,0) * C(n,0) = 1 way
    # 2. w = n, w' = n (all white): C(n,n) * C(n,n) = 1 way
    # 3. 0 < w < n and 0 < w' < n: sum over w=1..n-1, w'=1..n-1 of C(n,w) * C(n,w')
    
    from math import comb
    
    # Case 1 and 2: 2 configurations
    count = 2
    
    # Case 3: 
    # sum_{w=1}^{n-1} C(n,w) * sum_{w'=1}^{n-1} C(n,w')
    # = (2^n - 2) * (2^n - 2)
    # = (2^n - 2)^2
    
    total_row_configs = sum(comb(n, w) for w in range(1, n))  # 2^n - 2
    total_col_configs = sum(comb(n, w) for w in range(1, n))  # 2^n - 2
    
    count += total_row_configs * total_col_configs
    
    return count

result = solve(5)

# 调用 solve
result = solve(inputs['grid_size'])
print(result)