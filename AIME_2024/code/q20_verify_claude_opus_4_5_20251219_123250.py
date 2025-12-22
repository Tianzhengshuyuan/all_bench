inputs = {'grid_size': 5}

from math import comb

def solve(grid_size):
    n = grid_size
    
    # We need to count valid configurations where:
    # 1. Each cell has at most one chip
    # 2. All chips in same row have same color
    # 3. All chips in same column have same color
    # 4. No additional chip can be placed without violating conditions (maximality)
    
    # Each row can be: empty (E), white (W), or black (B)
    # Each column can be: empty (E), white (W), or black (B)
    # A chip exists at (i,j) iff row i and column j are both non-empty and have the same color
    
    # For maximality:
    # - If row i is empty and column j is empty: can add any chip -> not maximal (unless blocked)
    # - If row i is empty and column j has color c: can add chip of color c -> not maximal (unless blocked)
    # - If row i has color c and column j is empty: can add chip of color c -> not maximal (unless blocked)
    # - If row i has color c1 and column j has color c2 with c1 != c2: cannot add chip (blocked)
    # - If row i has color c and column j has color c: cell already has chip
    
    # For an empty row to be blocked: need columns of BOTH colors (so no single color works)
    # For an empty column to be blocked: need rows of BOTH colors
    # For an empty row AND empty column intersection: need both colors in rows AND both colors in columns
    
    # Let w_r = # white rows, b_r = # black rows, e_r = # empty rows
    # Let w_c = # white columns, b_c = # black columns, e_c = # empty columns
    
    # Constraints:
    # 1. If w_r > 0, need w_c > 0 (white rows need white columns)
    # 2. If b_r > 0, need b_c > 0 (black rows need black columns)
    # 3. If w_c > 0, need w_r > 0 (white columns need white rows)
    # 4. If b_c > 0, need b_r > 0 (black columns need black rows)
    # 5. If e_r > 0, need w_c > 0 AND b_c > 0 (empty rows blocked by both column colors)
    # 6. If e_c > 0, need w_r > 0 AND b_r > 0 (empty columns blocked by both row colors)
    # 7. If e_r > 0 AND e_c > 0, the intersection of empty row and empty column must be blocked
    #    This requires: we can't add any chip there. 
    #    If we try to add white: row becomes white, needs white column - but there are black columns
    #    If we try to add black: row becomes black, needs black column - but there are white columns
    #    Actually, we need to ensure that making the empty row any color would conflict.
    #    Since we already have both w_c > 0 and b_c > 0 (from constraint 5), 
    #    and both w_r > 0 and b_r > 0 (from constraint 6),
    #    the empty cell at (empty_row, empty_col) cannot be filled because:
    #    - If we add white chip: row becomes white, but there's a black column, conflict at that intersection
    #    - If we add black chip: row becomes black, but there's a white column, conflict at that intersection
    #    So constraints 5 and 6 together handle the case of e_r > 0 and e_c > 0.
    
    total = 0
    
    for w_r in range(n + 1):
        for b_r in range(n + 1 - w_r):
            e_r = n - w_r - b_r
            for w_c in range(n + 1):
                for b_c in range(n + 1 - w_c):
                    e_c = n - w_c - b_c
                    
                    # Constraints 1-4: color matching
                    if w_r > 0 and w_c == 0:
                        continue
                    if b_r > 0 and b_c == 0:
                        continue
                    if w_c > 0 and w_r == 0:
                        continue
                    if b_c > 0 and b_r == 0:
                        continue
                    
                    # Constraint 5: empty rows need both column colors
                    if e_r > 0 and not (w_c > 0 and b_c > 0):
                        continue
                    
                    # Constraint 6: empty columns need both row colors
                    if e_c > 0 and not (w_r > 0 and b_r > 0):
                        continue
                    
                    # Need at least one chip (non-empty configuration)
                    # If w_r = b_r = 0 or w_c = b_c = 0, no chips placed
                    if (w_r == 0 and b_r == 0) or (w_c == 0 and b_c == 0):
                        continue
                    
                    # Count ways to assign rows and columns
                    ways = comb(n, w_r) * comb(n - w_r, b_r) * comb(n, w_c) * comb(n - w_c, b_c)
                    total += ways
    
    return total

result = solve(5)

# 调用 solve
result = solve(inputs['grid_size'])
print(result)