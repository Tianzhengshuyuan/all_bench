inputs = {'grid_size': 5}

def solve(grid_size):
    """
    Solve the chip placement problem on a grid_size x grid_size grid.
    
    Conditions:
    1. Each cell contains at most one chip
    2. All chips in the same row have the same color
    3. All chips in the same column have the same color
    4. Any additional chip placed on the grid would violate one or more of the previous two conditions.
    
    The key insight from the hint is to do casework on columns.
    
    For maximality, every empty cell must be "blocked" - meaning we cannot add any chip there.
    An empty cell (i,j) is blocked only if row i has one color and column j has the other color.
    
    Let's think about this more carefully:
    - Each row can be: White (W), Black (B), or Empty (E)
    - Each column can be: White (W), Black (B), or Empty (E)
    - Cell (i,j) has a chip iff row[i] and col[j] are both non-empty and same color
    
    For maximality, for each empty cell (i,j):
    - If row[i]=E or col[j]=E, we can add a chip -> NOT maximal (unless blocked by other constraint)
    - If row[i]=W and col[j]=B (or vice versa), cell is blocked
    
    So we need: for every empty cell, row and column have opposite non-empty colors.
    
    This means:
    - No row can be empty (otherwise any cell in that row with non-empty column allows a chip)
    - No column can be empty
    - Every row is W or B, every column is W or B
    - Cell (i,j) has chip iff row[i] == col[j]
    
    For each row to have at least one chip (so it has a defined color):
    - If row i is W, need at least one column that is W
    - If row i is B, need at least one column that is B
    
    Similarly for columns.
    
    Let w = # white rows, b = n-w = # black rows
    Let w' = # white columns, b' = n-w' = # black columns
    
    Valid iff:
    - w > 0 implies w' > 0 (white rows need white columns)
    - b > 0 implies b' > 0 (black rows need black columns)
    - w' > 0 implies w > 0 (white columns need white rows)
    - b' > 0 implies b > 0 (black columns need black rows)
    
    This simplifies to: (w=0 iff w'=0) and (w=n iff w'=n)
    
    Valid cases:
    - w=0, w'=0: all black -> 1 way
    - w=n, w'=n: all white -> 1 way  
    - 0 < w < n and 0 < w' < n: mixed
    
    For mixed case, we choose which w rows are white (C(n,w) ways) and which w' columns are white (C(n,w') ways).
    
    Total for mixed = sum_{w=1}^{n-1} sum_{w'=1}^{n-1} C(n,w) * C(n,w') = (2^n - 2)^2
    
    Total = 2 + (2^n - 2)^2
    
    For n=5: 2 + 30^2 = 2 + 900 = 902
    
    But this gives 902 which seems to be wrong. Let me reconsider.
    
    Actually, re-reading the problem and hint about "casework on the column on the left",
    perhaps we need to consider that rows/columns CAN be empty in certain configurations.
    
    Let me reconsider: A row is "blocked" if it cannot receive any more chips.
    A row with white chips is blocked for black chips.
    A row with black chips is blocked for white chips.
    An empty row is not blocked for either color.
    
    For maximality, every empty cell must be blocked for BOTH colors.
    Cell (i,j) blocked for white: row i has black OR column j has black
    Cell (i,j) blocked for black: row i has white OR column j has white
    Cell (i,j) blocked for both: (row i has black OR col j has black) AND (row i has white OR col j has white)
    
    This means: {row_i, col_j} must contain both colors (as a set).
    So either row_i and col_j have opposite colors, OR one of them has both colors (impossible for a single row/col).
    
    So for each empty cell, row and column must have opposite colors (both non-empty).
    This confirms: no empty rows, no empty columns.
    
    The answer should be 2 + (2^n - 2)^2 = 902 for n=5.
    
    But wait - maybe the problem is asking for something different. Let me check if 
    the two "all same color" cases should be counted as 1 (same pattern, different colors)?
    
    No, white and black chips are distinguishable, so all-white and all-black are different.
    
    Let me try a different interpretation: maybe we're counting chip PATTERNS (ignoring colors)?
    Then all-white and all-black give the same pattern (full grid).
    And for mixed cases, swapping colors gives the same pattern.
    
    Patterns = 1 + (2^n - 2)^2 / 2 = 1 + 450 = 451 for n=5.
    
    Still not matching. Let me try yet another approach based on the hint.
    
    The hint says "casework on the column on the left" and "There can be 5".
    This suggests counting by how many cells in the leftmost column have chips.
    
    For a valid maximal configuration, the leftmost column has some color (W or B).
    The cells with chips in column 0 are exactly those rows with the same color as column 0.
    
    Let me try: the answer might be 2 * (3^n - 1) based on a different model.
    For n=5: 2 * (243 - 1) = 2 * 242 = 484. Not matching either.
    
    Let me just return the computed value.
    """
    from math import comb
    
    n = grid_size
    
    # Based on careful analysis:
    # - All rows and columns must be non-empty (have a color W or B)
    # - Valid configurations: all same color (2 ways) + mixed ((2^n-2)^2 ways)
    
    count = 2  # all white, all black
    
    # Mixed cases: 0 < w < n white rows, 0 < w' < n white columns
    for w in range(1, n):
        for wp in range(1, n):
            count += comb(n, w) * comb(n, wp)
    
    return count


result = solve(5)

# 调用 solve
result = solve(inputs['grid_size'])
print(result)