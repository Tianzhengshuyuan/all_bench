inputs = {'grid_size': 5}

from math import comb

def solve(grid_size):
    n = grid_size
    
    # We need to count valid configurations where:
    # 1. Each cell has at most one chip
    # 2. All chips in same row have same color
    # 3. All chips in same column have same color
    # 4. No additional chip can be placed without violating conditions (maximality)
    
    # Key insight: We assign each row a state (empty, white, black) and each column a state.
    # A chip at (i,j) exists iff row i and column j have the same non-empty color.
    
    # For maximality, at any empty cell (i,j), we cannot place a chip.
    # Cases for cell (i,j):
    # - row i empty, col j empty: we could place any chip, so this must be blocked
    # - row i empty, col j has color c: we could place chip of color c, so blocked
    # - row i has color c, col j empty: we could place chip of color c, so blocked
    # - row i has color c1, col j has color c2, c1 != c2: already blocked (conflict)
    # - row i has color c, col j has color c: chip already there
    
    # For an empty row to be blocked from adding any chip:
    # If we try to add a white chip somewhere in that row, the row becomes white.
    # For this to be invalid, every column must either be black or empty.
    # But if a column is empty, adding white chip there would make both row and column white - valid!
    # So for empty row to be blocked: no empty columns, and columns have both colors.
    
    # Actually, let's think more carefully:
    # If row i is empty and we want to add a chip at (i,j):
    # - If col j is empty: we can add any chip, row i becomes that color, col j becomes that color. Valid!
    # - If col j has color c: we add chip of color c, row i becomes color c. Valid!
    # So if row i is empty, we can always add a chip unless... there's a conflict.
    
    # The conflict arises when: if we make row i white, there's a black column (conflict at intersection).
    # And if we make row i black, there's a white column (conflict at intersection).
    # So empty row is blocked iff both white and black columns exist.
    # Similarly, empty column is blocked iff both white and black rows exist.
    
    # But wait, if row i is empty and col j is empty, we can add a chip there making both white (or both black).
    # This is valid! So we need: if there are empty rows AND empty columns, we can add a chip.
    # Therefore: we cannot have both empty rows and empty columns simultaneously.
    
    total = 0
    
    for w_r in range(n + 1):
        for b_r in range(n + 1 - w_r):
            e_r = n - w_r - b_r
            for w_c in range(n + 1):
                for b_c in range(n + 1 - w_c):
                    e_c = n - w_c - b_c
                    
                    # Constraints for chips to exist where needed:
                    # If w_r > 0, need w_c > 0 (white rows need white columns for chips)
                    if w_r > 0 and w_c == 0:
                        continue
                    # If b_r > 0, need b_c > 0
                    if b_r > 0 and b_c == 0:
                        continue
                    # If w_c > 0, need w_r > 0
                    if w_c > 0 and w_r == 0:
                        continue
                    # If b_c > 0, need b_r > 0
                    if b_c > 0 and b_r == 0:
                        continue
                    
                    # Maximality: empty rows blocked iff both w_c > 0 and b_c > 0
                    if e_r > 0 and not (w_c > 0 and b_c > 0):
                        continue
                    
                    # Maximality: empty columns blocked iff both w_r > 0 and b_r > 0
                    if e_c > 0 and not (w_r > 0 and b_r > 0):
                        continue
                    
                    # Cannot have both empty rows and empty columns (can add chip at intersection)
                    if e_r > 0 and e_c > 0:
                        continue
                    
                    # Need at least one chip
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