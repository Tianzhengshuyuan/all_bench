inputs = {'grid_size': 5}

from math import comb

def solve(grid_size):
    n = grid_size
    
    # We need to count valid configurations where:
    # 1. Each cell has at most one chip
    # 2. All chips in same row have same color
    # 3. All chips in same column have same color
    # 4. No additional chip can be placed without violating conditions (maximality)
    
    # Key insight: Each row can be in state: empty, white, or black
    # Each column can be in state: empty, white, or black
    # A chip exists at (i,j) iff row i and column j are both non-empty and have the same color
    
    # For maximality, we need to check when we can add a chip at an empty cell (i,j):
    # - If row i is empty and column j is empty: can add any chip -> not maximal
    # - If row i is empty and column j has color c: can add chip of color c -> not maximal
    # - If row i has color c and column j is empty: can add chip of color c -> not maximal
    # - If row i has color c1 and column j has color c2 with c1 != c2: cannot add chip (conflict)
    # - If row i has color c and column j has color c: cell already has chip
    
    # So for maximality with non-empty configuration:
    # - Every row must be non-empty
    # - Every column must be non-empty
    # - OR we need a special structure where empty rows/columns are "blocked"
    
    # An empty row i is blocked if there exist columns with both colors (white and black)
    # because we can't pick a single color for row i that works with all columns.
    # Similarly for empty columns.
    
    # Let W_r = set of white rows, B_r = set of black rows, E_r = set of empty rows
    # Let W_c = set of white columns, B_c = set of black columns, E_c = set of empty columns
    
    # For empty row to be blocked: need both W_c non-empty and B_c non-empty
    # For empty column to be blocked: need both W_r non-empty and B_r non-empty
    
    # Also need: if W_r non-empty, then W_c non-empty (so white rows have chips)
    # if B_r non-empty, then B_c non-empty (so black rows have chips)
    # if W_c non-empty, then W_r non-empty (so white columns have chips)
    # if B_c non-empty, then B_r non-empty (so black columns have chips)
    
    total = 0
    
    # Enumerate: w_r = |W_r|, b_r = |B_r|, e_r = |E_r| = n - w_r - b_r
    # w_c = |W_c|, b_c = |B_c|, e_c = |E_c| = n - w_c - b_c
    
    for w_r in range(n + 1):
        for b_r in range(n + 1 - w_r):
            e_r = n - w_r - b_r
            for w_c in range(n + 1):
                for b_c in range(n + 1 - w_c):
                    e_c = n - w_c - b_c
                    
                    # Check validity conditions
                    # 1. If w_r > 0, need w_c > 0 (white rows need white columns for chips)
                    if w_r > 0 and w_c == 0:
                        continue
                    # 2. If b_r > 0, need b_c > 0
                    if b_r > 0 and b_c == 0:
                        continue
                    # 3. If w_c > 0, need w_r > 0
                    if w_c > 0 and w_r == 0:
                        continue
                    # 4. If b_c > 0, need b_r > 0
                    if b_c > 0 and b_r == 0:
                        continue
                    
                    # 5. If e_r > 0 (empty rows exist), need both w_c > 0 and b_c > 0 to block them
                    if e_r > 0 and not (w_c > 0 and b_c > 0):
                        continue
                    # 6. If e_c > 0 (empty columns exist), need both w_r > 0 and b_r > 0 to block them
                    if e_c > 0 and not (w_r > 0 and b_r > 0):
                        continue
                    
                    # Count ways to assign rows and columns
                    ways = comb(n, w_r) * comb(n - w_r, b_r) * comb(n, w_c) * comb(n - w_c, b_c)
                    total += ways
    
    return total

result = solve(5)

# 调用 solve
result = solve(inputs['grid_size'])
print(result)