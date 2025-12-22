inputs = {'grid_size': 5}

from itertools import product

def solve(grid_size):
    n = grid_size
    
    # We need to place chips such that:
    # 1. Each cell contains at most one chip
    # 2. All chips in same row have same color
    # 3. All chips in same column have same color
    # 4. Grid is maximal - no additional chip can be placed without violating conditions
    
    # Each row can be: empty (E), has white chips (W), has black chips (B)
    # Each column can be: empty (E), has white chips (W), has black chips (B)
    # Cell (i,j) has a chip iff row[i] and col[j] are both non-empty AND same color
    
    # For maximality, every empty cell must be "blocked" - we cannot add any chip there.
    # For empty cell (i,j), we can add color c if:
    #   - row[i] is E or c, AND col[j] is E or c
    # Cell is blocked if for both colors, at least one of row/col has the opposite color.
    
    # Analyze blocking conditions for empty cell (i,j):
    # - row[i]=E, col[j]=E: can add any color -> NOT blocked
    # - row[i]=E, col[j]=W: can add white -> NOT blocked  
    # - row[i]=E, col[j]=B: can add black -> NOT blocked
    # - row[i]=W, col[j]=E: can add white -> NOT blocked
    # - row[i]=B, col[j]=E: can add black -> NOT blocked
    # - row[i]=W, col[j]=W: has chip (not empty)
    # - row[i]=B, col[j]=B: has chip (not empty)
    # - row[i]=W, col[j]=B: blocked (can't add white due to col, can't add black due to row)
    # - row[i]=B, col[j]=W: blocked
    
    # So for maximality: no empty rows, no empty columns allowed (unless grid is completely empty, 
    # but that's not maximal since we can add chips).
    
    # With all rows and columns non-empty:
    # - Each row is W or B
    # - Each column is W or B
    # - Cell (i,j) has chip iff row[i] == col[j]
    # - For row i with color c to have at least one chip, need at least one column with color c
    # - For column j with color c to have at least one chip, need at least one row with color c
    
    # Let's enumerate by the actual chip placement pattern.
    # We need to count distinct chip configurations, not (row_color, col_color) assignments.
    
    # Two different assignments can give the same chip pattern only if we swap all colors.
    # But swapping all row colors and all column colors gives the same pattern.
    # Actually no - if we swap row colors only, the pattern changes.
    
    # The chip pattern is determined by: which cells have chips.
    # Given a valid maximal configuration, the row colors and column colors are uniquely determined
    # by the chips (up to the choice of which color is "white" vs "black").
    
    # Actually, let's think differently. The problem asks for chip placements, not colorings.
    # Two colorings that produce the same set of occupied cells should count as one.
    
    # For a given (row_colors, col_colors), the occupied cells are {(i,j) : row[i] == col[j]}.
    # Swapping all colors (W<->B for all rows and columns) gives the same occupied cells.
    # So we're overcounting by factor of 2, except for the all-same-color cases.
    
    # All white (w=n, w'=n): swapping gives all black (w=0, w'=0). These are the same pattern!
    # Mixed cases: each pattern is counted twice.
    
    from math import comb
    
    # Total valid (row_colors, col_colors) assignments:
    # - All same color: 2 (all W or all B) -> but these give the same pattern (all cells filled)
    # - Mixed: (2^n - 2)^2 assignments, each pattern counted twice
    
    # So number of distinct patterns:
    # - 1 pattern for all cells filled
    # - (2^n - 2)^2 / 2 patterns for mixed cases
    
    # Wait, but we need to verify the mixed cases are all valid (every row and column has a chip).
    # For 0 < w < n and 0 < w' < n: every white row has a chip (since w' > 0), 
    # every black row has a chip (since b' = n - w' > 0), similarly for columns. Valid!
    
    # But wait - we also need to check that the pattern uniquely determines colors up to swap.
    # Given the occupied cells, can we recover the row/column colors?
    # Row i has color W iff it has a chip in some column j that is W.
    # This creates a dependency. Let's think about it as a bipartite graph.
    
    # Actually, the issue is more subtle. Let me reconsider.
    
    # The occupied cells form a pattern where cell (i,j) is occupied iff row[i] == col[j].
    # This is equivalent to: rows are partitioned into two groups (W and B), 
    # columns are partitioned into two groups (W and B),
    # and occupied cells are the "matching" pairs.
    
    # Given the occupied cells, can we recover the partition? 
    # The occupied cells form a "complete bipartite-like" structure within each color class.
    # If we know which rows are W, the columns with chips in those rows must be W.
    # So the coloring is determined up to swapping W<->B globally.
    
    # Therefore, each chip pattern corresponds to exactly 2 colorings (except all-filled which is 2 colorings but same pattern).
    
    total_colorings = 2 + (2**n - 2)**2  # all-same + mixed
    # all-same: 2 colorings, 1 pattern
    # mixed: (2^n-2)^2 colorings, (2^n-2)^2 / 2 patterns
    
    count = 1 + (2**n - 2)**2 // 2
    
    return count

result = solve(5)

# 调用 solve
result = solve(inputs['grid_size'])
print(result)