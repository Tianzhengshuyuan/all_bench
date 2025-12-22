inputs = {'grid_size': 5}

from itertools import product

def solve(grid_size):
    n = grid_size
    
    # We need to count valid configurations where:
    # 1. Each cell has at most one chip
    # 2. All chips in same row have same color
    # 3. All chips in same column have same color
    # 4. No additional chip can be placed without violating conditions
    
    # For each row, it can be: empty, all white chips, or all black chips
    # For each column, it can be: empty, all white chips, or all black chips
    # A chip at (i,j) exists iff row i is non-empty AND column j is non-empty AND they have same color
    
    # Let's enumerate: for each row, state in {0: empty, 1: white, 2: black}
    # For each column, state in {0: empty, 1: white, 2: black}
    
    # Condition 4 (maximality): 
    # - If a row is empty, then for every column that has chips, adding a chip of that column's color would violate something
    #   This means: if row i is empty and column j is non-empty (color c), we can't add chip at (i,j)
    #   But we CAN add a chip there if we make row i have color c. So row i being empty means we can extend it.
    #   Unless... every non-empty column has a different requirement that conflicts.
    #   Actually, for row i to be validly empty, all non-empty columns must have BOTH colors present among them,
    #   so that row i cannot pick a single color that works for all non-empty columns.
    
    # Let me reconsider: A configuration is maximal if we cannot add any chip.
    # Adding a chip at (i,j) requires:
    # - Cell (i,j) is empty
    # - After adding, row i has all same color and column j has all same color
    
    # If row i is currently empty and column j is currently empty, we can add any color chip at (i,j). So this violates maximality.
    # If row i is empty and column j has color c, we can add a chip of color c at (i,j) (making row i have color c). Violates maximality.
    # If row i has color c and column j is empty, we can add a chip of color c at (i,j). Violates maximality.
    # If row i has color c1 and column j has color c2:
    #   - If c1 == c2, then (i,j) must already have a chip (otherwise we could add one)
    #   - If c1 != c2, then (i,j) must be empty (can't have chip of two colors), and we can't add a chip there. Good.
    
    # So for maximality:
    # 1. No row can be empty if any column is empty (and vice versa) - unless ALL rows or ALL columns are empty
    # 2. If row i has color c1 and column j has color c2 and c1 == c2, then (i,j) has a chip
    # 3. If row i has color c1 and column j has color c2 and c1 != c2, then (i,j) is empty
    
    # Actually, let's reconsider condition for empty rows/columns:
    # If row i is empty and there exists a non-empty column j with color c, we can place chip of color c at (i,j).
    # This makes row i have color c. This is valid. So maximality is violated.
    # Therefore: if any row is empty, all columns must be empty. And vice versa.
    # This means: either the grid is completely empty, or no row is empty and no column is empty.
    
    # Case 1: Grid is empty. Is this maximal? We can add any chip anywhere. So NO, not maximal.
    
    # Case 2: No row is empty, no column is empty.
    # Each row has a color (W or B), each column has a color (W or B).
    # Chip at (i,j) iff row_color[i] == col_color[j].
    # This is automatically maximal because:
    # - If row_color[i] == col_color[j], there's already a chip at (i,j)
    # - If row_color[i] != col_color[j], we can't add a chip there (would need to match both colors)
    
    # So we need to count: number of ways to assign colors to rows and columns such that
    # each row has at least one chip and each column has at least one chip.
    
    # Row i has a chip iff there exists column j with same color.
    # Column j has a chip iff there exists row i with same color.
    
    # Let's say r_w = number of white rows, r_b = number of black rows, r_w + r_b = n
    # Let's say c_w = number of white columns, c_b = number of black columns, c_w + c_b = n
    
    # For each white row to have a chip, we need c_w >= 1.
    # For each black row to have a chip, we need c_b >= 1.
    # For each white column to have a chip, we need r_w >= 1.
    # For each black column to have a chip, we need r_b >= 1.
    
    # So we need: if r_w > 0 then c_w > 0, if r_b > 0 then c_b > 0, if c_w > 0 then r_w > 0, if c_b > 0 then r_b > 0.
    # This simplifies to: (r_w > 0 iff c_w > 0) and (r_b > 0 iff c_b > 0).
    
    # Cases:
    # A) r_w = n, r_b = 0 (all rows white): need c_w > 0, c_b = 0. So c_w = n. All white.
    # B) r_w = 0, r_b = n (all rows black): need c_b > 0, c_w = 0. So c_b = n. All black.
    # C) 0 < r_w < n and 0 < r_b < n: need c_w > 0 and c_b > 0, i.e., 0 < c_w < n.
    
    from math import comb
    
    # Case A: All rows white, all columns white. 1 way.
    # Case B: All rows black, all columns black. 1 way.
    # Case C: Choose which rows are white (r_w from 1 to n-1), choose which columns are white (c_w from 1 to n-1).
    #         Number of ways = sum over r_w=1 to n-1 of C(n, r_w) * sum over c_w=1 to n-1 of C(n, c_w)
    #                        = (2^n - 2) * (2^n - 2)
    
    count = 2 + (2**n - 2) * (2**n - 2)
    
    return count

result = solve(5)

# 调用 solve
result = solve(inputs['grid_size'])
print(result)