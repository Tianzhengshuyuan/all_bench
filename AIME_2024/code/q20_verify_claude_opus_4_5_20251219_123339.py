inputs = {'grid_size': 5}

from math import comb

def solve(grid_size):
    n = grid_size
    
    # We need to count valid configurations where:
    # 1. Each cell has at most one chip
    # 2. All chips in same row have same color
    # 3. All chips in same column have same color
    # 4. No additional chip can be placed without violating conditions (maximality)
    
    # Key insight: Each row can be: empty, white, or black
    # Each column can be: empty, white, or black
    # A chip exists at (i,j) iff row i and column j are both non-empty and have the same color
    
    # For maximality:
    # - At any empty cell (i,j), we cannot place a chip without violating conditions
    
    # Let's think about when we CAN'T add a chip at empty cell (i,j):
    # - If row i has color c1 and col j has color c2 with c1 != c2: blocked by color conflict
    # - If row i is empty: adding a chip of color c would make row i have color c
    #   This is blocked if: for every color c, there exists a column with the opposite color
    #   i.e., both white and black columns exist
    # - If col j is empty: similarly, blocked if both white and black rows exist
    # - If both row i and col j are empty: we can add any chip, making both that color
    #   This is blocked if: for any color c we choose, there's a conflict
    #   If we choose white: need a black column to conflict -> need b_c > 0
    #   If we choose black: need a white column to conflict -> need w_c > 0
    #   AND similarly for rows: need w_r > 0 and b_r > 0
    #   So blocked iff w_r > 0 AND b_r > 0 AND w_c > 0 AND b_c > 0
    
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
                    
                    # If both empty rows and empty columns exist:
                    # Need all four: w_r > 0, b_r > 0, w_c > 0, b_c > 0
                    # This is already guaranteed by the above two conditions when e_r > 0 and e_c > 0
                    
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